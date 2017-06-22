'use strict';

import gulp       from 'gulp';
import sass       from 'gulp-sass';
import maps       from 'gulp-sourcemaps';
import browserify from 'browserify';
import babelify   from 'babelify';
import source     from 'vinyl-source-stream';
import buffer     from 'vinyl-buffer';
import rename     from 'gulp-rename';
import glob       from 'glob'
import es         from 'event-stream';


gulp.task("styles", () => {
    gulp.src('./client/scss/app.scss')
        .pipe(maps.init())
        .pipe(sass())
        .pipe(maps.write('./'))
        .pipe(gulp.dest('./app/static/styles'));
});

// handle es6 modules and bundeling
gulp.task('js', (done) => {
    glob('./client/js/pages/*.js', (err, files) => {
        if (err) done(files);
        console.log(files);

        let tasks = files.map((entry) => {
            // set up the browserify instance on a task basis
            return browserify({
                entries: entry,
                debug: true,
                transform: [babelify]
            })
            .bundle()
            .pipe(source(entry))
            .pipe(buffer())
            .pipe(maps.init({loadMaps: true}))
            .pipe(rename({
                dirname: '',    // remove src dir stracture
                extname: '.bundle.js'
            }))
            .pipe(maps.write('./'))
            .pipe(gulp.dest('./app/static/js'));
        });
        es.merge(tasks).on('end', done);
    });
});

gulp.task('watch', function () {
    gulp.watch('./client/js/*.js', ['js']);
    gulp.watch('./client/scss/**/*.scss', ['styles']);
});

gulp.task('build', ['styles', 'js']);

gulp.task('default', ['watch']);