'use strict';

import gulp from 'gulp';
import sass from 'gulp-sass';
import maps from 'gulp-sourcemaps';
import babel from 'gulp-babel'

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
let babelify = require('babelify');
let source = require('vinyl-source-stream');
let rename = require('gulp-rename');
let glob = require('glob')
let es = require('event-stream');


// handle es6 including imports.
gulp.task('es6', (done) => {
    // Get all pages files
    glob('./client/pages/*.js', (err, files) => {
        if (err) done(files);
        console.log(files);

        let tasks = files.map((entry) => {
            // Browser side moduling
            return browserify({
                entries: entry,
                debug: true   
            })
            // Browserify transform for Babel (support es6 modules)
            .transform(babelify)
            .bundle()
            .pipe(source(entry))
            .pipe(rename({
                dirname: 'pages',
                extname: '.bundle.js'
            }))
            .pipe(gulp.dest('./app/static'));
        });
        es.merge(tasks).on('end', done);
    });
});

gulp.task('watch', function () {
    gulp.watch('**/*.js', ['es6'])
});

gulp.task('default', ['watch']);