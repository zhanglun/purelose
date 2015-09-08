var gulp = require('gulp');
var sass = require('gulp-sass');
var mainBowerFiles = require('main-bower-files');

var paths = {
    bowerFiles: './bower_components',
    scss: './static/assets/scss/**/*.scss',
    build: './static/build/'
};

gulp.task('sass', function () {
    gulp.src(paths.scss)
        .pipe(sass())
        .pipe(gulp.dest(paths.build + '/css'));
});

gulp.task('bower', function(){
    return gulp.src(mainBowerFiles(), {base: paths.bowerFiles})
        .pipe(gulp.dest('static/build/vendor'));
});

gulp.task('default', function(){
   gulp.watch('static/assets/scss/**/*.scss', ['sass']);
    gulp.watch(paths.bowerFiles, ['bower'])
});
