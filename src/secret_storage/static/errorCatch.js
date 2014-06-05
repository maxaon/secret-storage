/**
 * Created by Maxaon on 5/28/2014.
 */
window.onerror = function (msg, source, line, position, ex) {
  if (ex) {
    console.error(ex.message);

//  return true
  }
};
function scope(el) {
  var res = {};
  _.forOwn(scoper(el), function (v, k) {
    if (k.indexOf("$$") == 0)
      return
    res[k] = v;
  });
  return res;
}
function scoper(el) {
  return angular.element(el).scope()
}