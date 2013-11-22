from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder

from django.http import HttpResponse, HttpResponseBadRequest, Http404

from ajaxuploader.backends.local import LocalUploadBackend

class AjaxFileUploader(object):
    def __init__(self, backend=None, **kwargs):
        if backend is None:
            backend = LocalUploadBackend
        self.get_backend = lambda: backend(**kwargs)

    def __call__(self,request):
        return self._ajax_upload(request)

    def _ajax_upload(self, request):
        if request.method == "POST":
            
            # --------------------------------------
            # --- Ajax request                  ---- 
            if request.is_ajax():
                upload = request
                is_raw = True
                try:
                    filename = request.GET['qqfile']
                except KeyError:
                    return HttpResponseBadRequest("AJAX request not valid")
                
            # -------------------------------------------------------------
            # not an ajax upload, so it was the "basic" iframe version with
            # submission via form
            else:
                is_raw = False
                if len(request.FILES) == 1:
                    upload = request.FILES.values()[0]
                else:
                    raise Http404("Bad Upload")
                filename = upload.name

            # -------------------------------------------
            # --- process the Uploaded file           ---
            backend = self.get_backend()                                               # instantiate Backend class 
            filename = (backend.update_filename(request, filename) or filename)        # custom filename handler
            backend.setup(filename)                                                    # save the file
            success = backend.upload(upload, filename, is_raw)                         # upload file
            extra_context = backend.upload_complete(request, filename)                 # callback
            sizeFile = backend.size_file()                                             # return size of upoloaded file
            ret_json = {'success': success, 'filename': filename , 'size' : sizeFile}  # let Ajax Upload know whether we saved it or not

            if extra_context is not None:
                ret_json.update(extra_context)

            return ret_json
