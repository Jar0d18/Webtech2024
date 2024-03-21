const gulp = require('gulp');
const concat = require('gulp-concat');

function mergeCSS() {
    return gulp.src('C:/users/Jarod/Desktop/Webtechnologie/website/static/**/*.css') // Pas het pad aan naar je CSS-bestanden
        .pipe(concat('bungalow.css')) // Geef het gecombineerde bestand een naam
        .pipe(gulp.dest('C:/users/Jarod/Desktop/Webtechnologie/website/static'));
}

exports.default = mergeCSS; 


