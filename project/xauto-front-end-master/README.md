HTML5 / AngularJS front end client
===============
***

## Setup the project

Install Node.js and then:
```sh
$ git clone git://git@github.com:willandre/xauto-front-end.git
$ cd xauto-front-end
$ sudo npm -g install grunt-cli karma bower
$ npm install
$ bower install
$ grunt watch
```


Here can be an error with grunt-karma version, it can stop installation process and after here will be different errors.
It depends on operation system, in my case solutions is: set "grunt-karma": "0.8.0" in package.json

Finally, open `file:///[path-to-project]/build/index.html` in your browser.

Happy hacking!

