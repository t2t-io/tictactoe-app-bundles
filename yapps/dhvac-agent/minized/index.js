// Generated by LiveScript 1.5.0
(function(){
  var app;
  if (process.env['TIME_REQUIRE'] != null) {
    require('time-require');
    global.yapBaseappStartHook = global.yapWebappStartHook = function(err){
      return process.exit(0);
    };
  }
  app = process.env['APP_BUNDLE_JS'] != null
    ? require(process.env['APP_BUNDLE_JS'])
    : require('./app/bundle');
}).call(this);
