  module.exports = function(grunt) {
  require('load-grunt-tasks')(grunt);
  require('time-grunt')(grunt);

  // array of custom javascript files to include.
  var jsApp = [
    'js/scripts.js',
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
        'profiles/static/css/style.css': 'profiles/static/css/style.scss'
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
          'js/app.min.js': [jsApp]
        }
      }
    },

    watch: {
      grunt: {
        files: ['Gruntfile.js']
      },
      scss: {
        files: 'profiles/static/css/*.scss',
        tasks: ['sass'],
      }
    }
    
  });

  grunt.registerTask('build', ['sass','jshint','uglify']);
  grunt.registerTask('default', ['build']);

};
