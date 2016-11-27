from skills.models import Skill
from skillsets.models import Skillset

__all__ = ["CSS_SKILLS"]


CSS_SKILLS = {
    Skillset: {
        Skill: [{
            "name": "Basic CSS Edits",
            "description": "You could open a CSS file and change the font-size of a heading. You might be able to tweak the CSS of page through a CMS like Wordpress or Drupal.",
            "weight": 1
        }, {
            "name": "Basic Static Page",
            "description": "Someone gives you a Photoshop mockup of a basic 1 column landing page with a few headings, a bullet list and some images. You could implement said design as static HTML and CSS. You are familiar with writing CSS and the common properties in the older CSS2 spec, ie background:, margin: etc.", 
            "weight": 2
        },{
            "name": "CSS Inheritance and Specificity",
            "description": "You have a solid understanding of CSS inheritance and specificity. You can calculate the specificity of a selector based on it’s location, id, class and levels of nesting. You understand how inline css, css declared in <style> and css declared in a file affect specificity.  Use Chrome dev tools or firebug to inspect elements and their styles.",
            "weight": 3
        },{
            "name": "Layout, Floats, Display, Box Model",
            "description": "The pillars of website design. You are familiar with using display and float to create complex, nested div layouts. You can visually outline and draw templates on paper or in your mind. You understand the difference between inline and block level elements and which elements are by default inline or block. You understand float and how to use float to create grids, columns and stacked layouts.", 
            "weight": 4
        },{
            "name": "Absolute Positioning, Z-Index",
            "description": "You understand how to use absolute, relative and fixed positioning. You understand how z-index affects the depth of the page and how to overlay elements below or on top of other elements. You understand the pitfalls of absolute positioning because of how it effects the document flow and when and where using absolute positioning is worthwhile.",
            "weight": 5
        },{
            "name": "CSS3",
            "description": "You can use modern CSS3 features, including. Gradients, multiple backgrounds, truncation and ellipse, box and text shadow, transition and animation. You have implemented a card or grid layout using flexbox or grid. You have command over popular pseudo elements such as :before, :after, :nth-child, :last-of-type. You understand how the > and + operators work.",
            "weight": 6
        },{
            "name": "Cross-Browser Compatibility",
            "description": "From experience you know the common pitfalls and likely compatibility issues when using certain CSS properties or layout patterns. You are able to assess which properties are safe on a project given a level of the required browser support. Implement a grid system which is compatible with IE9. Use vendor prefixes. Have experienced and attempted to “fix” form fields, select boxes and buttons across different browsers and mobile devices (iphone, tablet) etc.",
            "weight": 7
        },{
            "name": "Pre Compilers (SCSS, LESS)",
            "description": "You regularly use a CSS pre-compiler. You can setup a compiler using GUI or CLI and watch for changes. You can use variables, includes, mixins, extends, nesting and variables. You can structure a project to use multiple files and import and compile files in the correct order.",
            "weight": 8
        },{
            "name": "CSS Synthesis ",
            "description": "You have implemented many different CSS frameworks and methodologies. You have spent time reflecting upon the pros and cons of the various approaches. You have developed a paradigm for writing CSS that has been proven to be useful on a large scale project over time. You and the members of your team have seen improved maintainability, productivity gains and and a better product due to it’s use.",
            "weight": 9
        }, {
            "name": "You Are A Recognized Industry Expert",
            "description": "You are a well known speaker, writer and thought leader (like Jeffrey Zeldman?). You are a core contributor to the language/specification or created an open source library or framework which is synonymous with the language (ie SCSS, Bootstrap etc).",
            "weight": 10
        }]
    }
}