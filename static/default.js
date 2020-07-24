$( document ).ready(function() {

   var observer = new MutationObserver(function(mutation){
     console.log('Change detected');
     console.log(mutation);
     window.location.replace("http://127.0.0.1:5000/logout");
     });

     observer.observe(document.querySelector('#postBtn'), {
        childList: true,
        attributes: true,
        subtree: true,
        characterData: true,
        attributeOldValue: true,
        characterDataOldValue: true
     });

     observer.observe(document.querySelector('#searchBtn'), {
       childList: true,
       attributes: true,
       subtree: true,
       characterData: true,
       attributeOldValue: true,
       characterDataOldValue: true
     });
});
