# ----------------------------
# --- Main Django library ----
from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.files.uploadedfile import UploadedFile

try:
    import json
except:
    from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.views.decorators.cache import cache_page, never_cache
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.template import RequestContext

# -----------------------
# --- xauto Models ---
from models import MultiuploaderImage
from models import MultiuploaderFiles
from xauto_lib.decorators import json_view, post_required


# ---------------------------------
# --- for generating thumbnails ---
from sorl.thumbnail import get_thumbnail
from event.models import Event
from member.models import UserProfile, Message
from lib.utils import CheckNumeric

# ----------------------
# --- ajax Uploader ----
from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.backends.thumbnail import ThumbnailUploadBackend

# ------------------------------------
# --- Main standard Python Library ---
import logging
import string

log = logging


@csrf_exempt
@never_cache
def ajaxUploader(request):
    """
    Ajax Uploader
    """

    category_image = request.GET.get('category', 'team')
    category_file = request.GET.get('type', 'image')
    event_id  = request.GET.get('event')
    message_id  = request.GET.get('message')
    currentUser = request.user

    # ------------------------------------------------
    # -- Backend Upload process                    ---
    if category_file == 'image':
        import_uploader = AjaxFileUploader(backend=ThumbnailUploadBackend, DIMENSIONS="500x500", KEEP_ORIGINAL=True)
    else:
        import_uploader = AjaxFileUploader()
    response_data = import_uploader._ajax_upload(request)

    # --------------------------------------
    # --- retreive File Characterictics  ---
    filename = response_data['filename']
    arrayFile = string.split(filename, '.')
    sizeFile = response_data['size']
    pathStore = settings.MULTI_IMAGES_FOLDER +'/'
    image = None
    eventObject = None
    messageObject = None

    # ---------------------------------------
    # --- Get Image List                  ---
    # --- user / team / Event / organizer ---
    userProfileObj = None
    image = None
    try:
        user = currentUser
        userProfileObj = UserProfile.objects.filter(user=user)

        # -- add an image to a user profile --
        if category_image in ('user', 'team'):
            imageList = MultiuploaderImage.objects.filter(userprofile=userProfileObj, application=category_image)

        # --- add an image to  a Event record ----
        elif category_image in ('event'):
            eventObject = Event.objects.filter(id=event_id)
            if eventObject:
                imageList = MultiuploaderImage.objects.filter(userprofile=userProfileObj, application=category_image, event=eventObject[0])

        # --- retrieve the current Image if exist ---
        if imageList:
            image = imageList[0]
    except:
        pass

    # -----------------------------------------
    # --- Get Message Object if provided    ---
    if message_id:
        try:
            if CheckNumeric(message_id):
                messageObject = Message.objects.get(pk=message_id)
        except:
            pass


    # ------------------------------------------------------------------
    # --- Add a new Image only one is allowed  (previous is deleted)  --
    # --- add a dynamic count of Event Image                            --
    if category_image in ('user'):
        if image:
            image.delete()

    # -------------------------------------------------------
    # ---- in all case create anew image or a New file  -----
    # ------ I M A G E    O N L Y     ----
    if category_file == 'image':
        image = MultiuploaderImage()
        image.filename = filename
        image.application = category_image
        image.image = pathStore + filename
        image.image_type = string.upper(arrayFile[1])
        image.caption = arrayFile[0]
        image.size = sizeFile
        image.key_data = image.key_generate
        if userProfileObj:
            image.userprofile = userProfileObj[0]
        if eventObject:
            image.event  = eventObject[0]
        image.save()
        fileKeyData = image.key_data
        fileId = image.pk

    # ------------------------------------------------------------
    # ------ A N Y      F I L E S  (without Image processing) ----
    else:
        filerecord = MultiuploaderFiles()
        filerecord.filename = filename
        filerecord.application = category_image
        filerecord.path = pathStore + filename
        filerecord.file_type = string.upper(arrayFile[1])
        filerecord.caption = arrayFile[0]
        filerecord.size = sizeFile
        filerecord.key_data = filerecord.key_generate
        filerecord.user = currentUser
        if eventObject:
            filerecord.event  = eventObject[0]
        # --- notice there is a message attached to the Uploaded file ----
        # --- notice there is a file attached to the current message
        if messageObject:
            filerecord.message = messageObject
            messageObject.attached = True
            messageObject.save()
        filerecord.save()
        fileKeyData = filerecord.key_data
        fileId = filerecord.pk

    # ---------------------------------------
    # --- add images (M2M) to userprofile ---
    if category_file == 'image':
        if userProfileObj:
            userProfileObj[0].images.add(image)
            userProfileObj[0].save()
    # -----------------------------------------
    # --- add Files (M2M) to message Models ---
    elif category_file == 'file':
        if filerecord and messageObject:
            messageObject.joined_files.add(filerecord)
            messageObject.save()


    # --------------------------
    # --- settings imports   ---
    try:
        file_delete_url = settings.MULTI_FILE_DELETE_URL+'/'
        file_url = settings.MULTI_IMAGE_URL+'/' + fileKeyData + '/'
    except AttributeError:
        file_delete_url = 'multi_delete/'
        file_url = 'multi_image/' + fileKeyData + '/'

    # ---------------------------------------------------
    # --- getting thumbnail url using sorl-thumbnail  ---
    thumb_url = ''
    if category_file == 'image':
        im = get_thumbnail(image, "80x80", quality=50)
        thumb_url = im.url

    # ----------------------------------------
    # --- return a formatted Json Object   ---
    result = {"size":sizeFile,
            "url":file_url,
            "thumbnail_url":thumb_url,
            "delete_url":file_delete_url+str(fileId)+'/',
            "delete_type":"POST",
            'success' :  True,
            }

    #return result

    # ---------------------------------------
    # ---- result results in Json  Format ---
    retJson = json.dumps(response_data, cls=DjangoJSONEncoder)
    contentType = 'application/json; charset=utf-8'
    #ret_json = { 'success': True, }
    return HttpResponse( retJson )



@csrf_exempt
def multiuploader(request):
    """
    Main MultiUploader module.
    Parses data from jQuery plugin and makes database changes.
    """
    if request.method == 'POST':
        log.info('received POST to main multiuploader view')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')

        # -------------------------------------------
        #getting file data for farther manipulations
        image =  None
        category_image = request.POST.get('category_images', 'team')
        file = request.FILES[u'files']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        arrayFile = string.split(filename, '.')

        # -------------------------------
        # --- save userprofile Info -----
        userProfileObj = None
        try:
            user = request.user
            userProfileObj = UserProfile.objects.filter(user=user)
            imageList = MultiuploaderImage.objects.filter(userprofile=user, application=category_image)
            if imageList:
                image = imageList[0]
        except:
            pass

        # ------------------------------------------------------------------
        # --- Add a new team Image or replace/add new Avatar image (user) --
        if category_image == 'user':
            if image:
                image.delete()

        # ----------------------------------------
        # ---- in all case create anew image -----
        image = MultiuploaderImage()
        image.filename=str(filename)
        image.application = category_image
        image.image=file
        image.image_type = string.upper(arrayFile[1])
        image.caption = arrayFile[0]
        image.size = round(file_size / 1024, 1)
        image.key_data = image.key_generate
        if userProfileObj:
            image.userprofile = userProfileObj[0]
        image.save()

        # -----------------------------------------
        #getting thumbnail url using sorl-thumbnail
        im = get_thumbnail(image, "80x80", quality=50)
        thumb_url = im.url

        # ------------------
        #settings imports
        try:
            file_delete_url = settings.MULTI_FILE_DELETE_URL+'/'
            file_url = settings.MULTI_IMAGE_URL+'/'+image.key_data+'/'
        except AttributeError:
            file_delete_url = 'multi_delete/'
            file_url = 'multi_image/'+image.key_data+'/'

        # ------------------------------
        #generating json response array
        result = []
        result.append({"name":filename,
                       "size":file_size,
                       "url":file_url,
                       "thumbnail_url":thumb_url,
                       "delete_url":file_delete_url+str(image.pk)+'/',
                       "delete_type":"POST",})
        response_data = simplejson.dumps(result)

        #checking for json data type
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else: #GET
        return HttpResponse('Only POST accepted')

def multi_show_uploaded(request, key):
    """Simple file view helper.
    Used to show uploaded file directly"""
    image = get_object_or_404(MultiuploaderImage, key_data=key)
    url = settings.MEDIA_URL+image.image.name
    return render_to_response('multiuploader/one_image.html', {"multi_single_url":url,})



@csrf_exempt
@json_view
def multiuploader_ajax(request):
    """
    Main MultiUploader module.
    Parses data from jQuery plugin and makes database changes.
    """

    # -------------------------------------------
    #getting file data for farther manipulations
    category_image = request.POST.get('category_images', 'team')
    file = request.FILES[u'file']
    wrapped_file = UploadedFile(file)
    filename = wrapped_file.name
    file_size = wrapped_file.file.size

    # -------------------------------
    # --- save userprofile Info -----
    userProfileObj = None
    try:
        user = request.user
        userProfileObj = UserProfile.objects.filter(user=user)
        imageList = MultiuploaderImage.objects.filter(userprofile=user)
    except:
        pass

    # ------------------------------------------
    # --- writing file manually into model   ---
    arrayFile = string.split(filename, '.')
    image = MultiuploaderImage()
    image.filename=str(filename)
    image.application = category_image
    image.image=file
    image.image_type = string.upper(arrayFile[1])
    image.caption = arrayFile[0]
    image.size = round(file_size / 1024, 1)
    image.key_data = image.key_generate
    if userProfileObj:
        image.userprofile = userProfileObj[0]
    image.save()

    # -----------------------------------------
    #getting thumbnail url using sorl-thumbnail
    im = get_thumbnail(image, "80x80", quality=50)
    thumb_url = im.url

    # ------------------
    #settings imports
    try:
        file_delete_url = settings.MULTI_FILE_DELETE_URL+'/'
        file_url = settings.MULTI_IMAGE_URL+'/'+image.key_data+'/'
    except AttributeError:
        file_delete_url = 'multi_delete/'
        file_url = 'multi_image/'+image.key_data+'/'

    # ------------------------------
    #generating json response array
    result = []
    result.append({"name":filename,
                    "size":file_size,
                    "url":file_url,
                    "thumbnail_url":thumb_url,
                    "delete_url":file_delete_url+str(image.pk)+'/',
                    "delete_type":"POST",})

    response_data = simplejson.dumps(result)
    return response_data



@csrf_exempt
@json_view
def multiuploader_delete(request, pk):
    """
    View for deleting photos with multiuploader AJAX plugin.
    made from api on:
    https://github.com/blueimp/jQuery-File-Upload
    """

    status = ''
    msg = ''
    count_file = 0
    type = ''

    if request.method == 'POST':
        mode = request.POST.get('mode')
        type = request.POST.get('type', 'image')

        log.info('Called delete image. image id='+str(pk))
        if type == 'image':
            image = get_object_or_404(MultiuploaderImage, pk=pk)
            image.delete()
            status = 'ok'
        else:
            # ------------------------------------------------------------
            # ---- Delete from message if attached                     ---
            # ---- if Linked to a message (Clean Message joined_files) ---
            fileObject = get_object_or_404(MultiuploaderFiles, pk=pk)

            if fileObject.message:
                messageObject = fileObject.message
                listAttached = messageObject.joined_files.filter(message=messageObject)
                if listAttached:
                    messageObject.joined_files.remove(fileObject)
                    messageObject.save()
                    listAttached = messageObject.joined_files.all()
                    if not listAttached:
                        messageObject.attached = False
                        messageObject.save()
                    else:
                        count_file = len(listAttached)

            fileObject.delete()
            status = 'ok'

        log.info('DONE. Deleted photo id='+str(pk))
        return {
            "status": status,
            "msg": msg,
            "type" : type,
            "count" : count_file,
        }
    else:
        log.info('Received not POST request to delete image view')
        return HttpResponseBadRequest('Only POST accepted')


@never_cache
@login_required
@json_view
def user_list_files(request):
    """
    Return list of files related to member/user.

    """

    template_name = 'multiuploader/block-files.html'
    currentUser= request.user
    application = request.GET.get('application')
    user_id = request.GET.get('user')
    message_id = request.GET.get('message')
    currentMessage = None

    if CheckNumeric(user_id):
        currentUser = User.objects.get(pk=user_id)
        if CheckNumeric(message_id):
            currentMessage = Message.objects.get(pk=message_id)


    # ----------------------------------------------------
    # --- extract all Images for the selected member -----
    if currentMessage:
        fileList = MultiuploaderFiles.objects.filter(user=currentUser, application=application, message=currentMessage)
    else:
        fileList = MultiuploaderFiles.objects.filter(user=currentUser, application=application)

    # ----------------------------------
    # ---- prepare Html rendering ------
    ctx = {
        'items': fileList,
        'ajax': True,
        'total_count': fileList.count(),
    }

    # -------------------------------------------
    # --- Html rendering                      ---
    html = render_to_string(template_name, ctx, context_instance=RequestContext(request))
    return {
        "html": html,
        "total_count": fileList.count(),
    }

