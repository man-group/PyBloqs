function isIE(){var myNav=navigator.userAgent.toLowerCase();return(myNav.indexOf('msie')!=-1)?parseInt(myNav.split('msie')[1]):false;}
var ieVersion=isIE();if(ieVersion&&ieVersion<10){alert("Internet Explorer 10 and older are not supported. Use Chrome, Firefox, Safari or IE 11 instead.");}
function blocksEval(data){(window.execScript||function(data){window["eval"].call(window,data);})(data);}
function registerWaitHandle(handle){if(!window.loadWaitHandleRegistry){window.loadWaitHandleRegistry={}}
loadWaitHandleRegistry[handle]=false;}
function setLoaded(handle){loadWaitHandleRegistry[handle]=true;}
function runWaitPoller(){var loadWaitPoller=setInterval(function(){if("loadWaitHandleRegistry"in window){var handleCount=0;for(var handle in loadWaitHandleRegistry){if(!loadWaitHandleRegistry.hasOwnProperty(handle)){handleCount++;if(!loadWaitHandleRegistry[handle]){return}}}}
clearInterval(loadWaitPoller);window.print();},10);return loadWaitPoller;}