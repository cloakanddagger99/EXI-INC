import*as e from"@wordpress/interactivity";var t={d:(e,o)=>{for(var r in o)t.o(o,r)&&!t.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:o[r]})},o:(e,t)=>Object.prototype.hasOwnProperty.call(e,t)};const o=(e=>{var o={};return t.d(o,e),o})({store:()=>e.store}),r=e=>{let t;try{t=new window.ActiveXObject(e)}catch(e){t=void 0}return t};(0,o.store)("core/file",{state:{get hasPdfPreview(){return!(window.navigator.userAgent.indexOf("Mobi")>-1||window.navigator.userAgent.indexOf("Android")>-1||window.navigator.userAgent.indexOf("Macintosh")>-1&&window.navigator.maxTouchPoints&&window.navigator.maxTouchPoints>2||(window.ActiveXObject||"ActiveXObject"in window)&&!r("AcroPDF.PDF")&&!r("PDF.PdfCtrl"))}}},{lock:!0});