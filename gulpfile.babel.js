'use strict';

import gulp from 'gulp';
import sass from 'gulp-sass';
import maps from 'gulp-sourcemaps';

const dirs = {
    src: 'app/static',
    dest: 'app/static'
};


gulp.task("hello", () => {
    console.log("Hello!");
});

gulp.task("styles", () => {
    const files = {
        src: `${dirs.src}/scss/app.sass`,
        dst: `${dirs.src}/css/app.css`
    };
    gulp.src(files.src)
        .pipe(maps.init())
        .pipe(sass())
        .pipe(maps.write('./'))
        .pipe(gulp.dest(files.dst));
});


let browserify = require('browserify');
let babelify   = require('babelify');
let source     = require('vinyl-source-stream');
let buffer     = require('vinyl-buffer');
let rename     = require('gulp-rename');
let glob       = require('glob')
let es         = require('event-stream');


// handle es6 modules and bundeling
gulp.task('javascript', (done) => {

    glob('./client/pages/*.js', (err, files) => {
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
                dirname: 'pages',
                extname: '.bundle.js'
            }))
            .pipe(maps.write('./'))
            .pipe(gulp.dest('./app/static'));
        });
        es.merge(tasks).on('end', done);
    });
});

gulp.task('watch', function () {
    gulp.watch('./client/**/*.js', ['javascript'])
});

gulp.task('default', ['watch']);