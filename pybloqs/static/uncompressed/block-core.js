function isIE () {
  var myNav = navigator.userAgent.toLowerCase();
  return (myNav.indexOf('msie') != -1) ? parseInt(myNav.split('msie')[1]) : false;
}

var ieVersion = isIE();

if (ieVersion && ieVersion < 10) {
    alert("Internet Explorer 10 and older are not supported. Use Chrome, Firefox, Safari or IE 11 instead.");
}

/* Global evaluation function a la jQuery */
function blocksEval(data) {
    (window.execScript || function (data) {
        window["eval"].call(window, data);
    })(data);
}

/* Registers a wait handle that can be used to signal when components have finished rendering */
function registerWaitHandle(handle) {
    if (!window.loadWaitHandleRegistry) {
        window.loadWaitHandleRegistry = {}
    }
    loadWaitHandleRegistry[handle] = false;
}

/* Set the supplied handle */
function setLoaded(handle) {
    loadWaitHandleRegistry[handle] = true;
}

/* Poll the wait handle list and wait until all the registered handles are set */
function runWaitPoller() {
    var loadWaitPoller = setInterval(function () {
        /* Check if the load wait handle registry exists */
        if ("loadWaitHandleRegistry" in window) {
            var handleCount = 0;

            /* Loop through handles in the registry */
            for (var handle in loadWaitHandleRegistry) {
                /* Skip properties */
                if (!loadWaitHandleRegistry.hasOwnProperty(handle)) {
                    handleCount++;
                    /* If a handle is unset, exit without quitting the poller */
                    if (!loadWaitHandleRegistry[handle]) {
                        return
                    }
                }
            }
        }

        /* Clear the poller and trigger printing */
        clearInterval(loadWaitPoller);
        /* Force the printing only if handle count is > 0 */
        window.print();

    }, 10);

    return loadWaitPoller;
}
