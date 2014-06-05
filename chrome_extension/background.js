/**
 * Created by Maxaon on 5/26/2014.
 */
var public_key = "";
chrome.webRequest.onBeforeRequest.addListener(
  function (details) {
    return {cancel: details.url.indexOf("://www.evil.com/") != -1};
  },
  {urls: ["http://localhost:8000/*"]},
  ["blocking"]);
