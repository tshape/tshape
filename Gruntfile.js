  module.exports = function(grunt) {
  require('load-grunt-tasks')(grunt);
  require('time-grunt')(grunt);

  // array of custom javascript files to include.
  var jsApp = [
    'src/tshape/static/js/scripts.js',
  ];

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    sass: {
      options: {
          outputStyle: 'expanded',
          sourceComments: true,
          sourceMap: false
      },
      dist: {
        files: { 
        'src/static/css/style.css': 'src/static/scss/style.scss'
        }
      }
    },

    jshint: {
      all: [
        'Gruntfile.js', jsApp
      ]
    },

    uglify: {
      options: {
        sourceMap: false,
        compress: false,
        beautify: false,
        preserveComments: 'some',
        mangle: false
      },
      dist: {
        files: {
          'src/tshape/static/js/app.min.js': [jsApp]
        }
      }
    },

    watch: {
      grunt: {
        files: ['Gruntfile.js']
      },
      scss: {
        files: 'src/static/**/*.scss',
        tasks: ['sass'],
      }
    }
    
  });

  grunt.registerTask('build', ['sass','jshint','uglify']);
  grunt.registerTask('default', ['build']);

};
