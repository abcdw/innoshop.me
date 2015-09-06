gulp = require 'gulp'
less = require 'gulp-less'
concat = require 'gulp-concat'
uglify = require 'gulp-uglify'

gulp.task 'less', ->
  gulp.src 'node_modules/bootstrap/less/bootstrap.less'
    .pipe less compress: true
    .pipe gulp.dest '../../innoshop/shop/static/css/'

gulp.task 'js', ->
  gulp.src [
    'node_modules/bootstrap/js/dropdown.js'
    'node_modules/bootstrap/js/collapse.js'
  ]
    .pipe concat 'bootstrap.js'
    .pipe do uglify
    .pipe gulp.dest '../../innoshop/shop/static/js'

gulp.task 'jquery', ->
  gulp.src 'node_modules/jquery/dist/jquery.min.js'
    .pipe gulp.dest '../../innoshop/shop/static/js'

gulp.task 'default', ['less', 'js']