from skills.models import Skill
from skillsets.models import Skillset

__all__ = ["HTML_SKILLS"]


HTML_SKILLS = {
    Skillset: {
        Skill: [{
            "name": "Basic Text HTML",
            "description": "You can write basic HTML in an editor or WYSIWYG editor (such as Wordpress). You can perform basic text styling using tags such as heading, paragraph and a bullet list. ",
            "weight": 1
        }, {
            "name": "Basic HTML Document",
            "description": "You can create a HTML document, using <html>, <body> tags. You can use <div> tags to create some basic sections and seperate content. You can use a wide range of tags to write some general content inside the document. You can save the document and view it in the browser.",
            "weight": 2
        },{
            "name": "HTML Library",
            "description": "You are familiar with most of the available and regularly use the entire range of HTML elements.",
            "weight": 3
        },{
            "name": "HTML Tables",
            "description": "You can write a HTML table.",
            "weight": 4
        },{
            "name": "HTML5 Layout Elements",
            "description": "You can use the new semantic elements that define the different parts of a web page: such as <header>, <nav>, <section> etc.",
            "weight": 5
        },{
            "name": "Block level vs. Inline tags",
            "description": "You understand the different between block and inline tags and which tags are naturally block or inline. You understand how block and inline tags are intended to be nested and the semantic structural reasoning behind this.",
            "weight": 6
        },{
            "name": "Forms, Input Elements and More",
            "description": "You can create static forms using all available input fields. You can describe a form and use inputs, select, checkbox, radio field etc. You can use input type, such as <input type=”text”>. You can use labels and fieldsets to layout a form. You understand when and why to use each type of input field. You can create a form submission button, but you do not need to build the functionality to submit and process the form, just the HTML form skeleton.",
            "weight": 7
        },{
            "name": "Semantic HTML",
            "description": "You understand the theory around semantic HTML. Why is semantic HTML important and how is it relevant today. You could describe practical situations in the context of software and publishing where semantic HTML might be advantageous.",
            "weight": 8
        },{
            "name": "HTML Fluency",
            "description": "You write HTML all the time, as part of other projects and general web development. Writing HTML is natural and easy for you. You can write HTML quickly without referencing the library and know when and where to use the appropriate tags and their their available attributes.",
            "weight": 9
        },{
            "name": "You Are A Recognized Industry Expert",
            "description": "You wrote a (well known) book, are a thought leader and speaker or are a core contributor to the language or created/core contributor to a library which is synonymous with the language.",
            "weight": 10
        }]
    }
}