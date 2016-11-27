from skills.models import Skill
from skillsets.models import Skillset

__all__ = ["JAVASCRIPT_SKILLS"]


JAVASCRIPT_SKILLS = {
    Skillset: {
        Skill: [{
            "name": "Snippets",
            "description": "You can embed an inline script tag in the head or body of a document or load an external Javascript file. Able to make simple modifications to Javascript code snippets and/or libraries; such as modifying a variable, changing a configuration object property or modifying the output of a text string.",
            "weight": 1
        }, {
            "name": "Variables, Basic Functions & Conditional Logic",
            "description": "You can write a basic function that accepts an argument and outputs a value. Declare both the function and then call the function. You can write a simple if/else statement. You can use comparison and logical operators to check multiple conditions and determine equality or difference between variables or values. Load and execute this code in the browser.",
            "weight": 2
        },{
            "name": "DOM Manipulation and Traversal",
            "description": "You understand the DOM, and can inspect the DOM using dev tools. You can select DOM elements using vanilla Javascript or jQuery (or another popular library). You could select an element and add a class so that the element shows/hides when you click on it. You can access and write to common properties of an element such as changing the innerHtml.",
            "weight": 3
        },{
            "name": "Arrays, Object Literals & Iteration",
            "description": "You can use Javascript (or jQuery/popular Library) to perform AJAX calls. You can get and post data from an API endpoint. You can write an AJAX call that get’s a JSON object from an API and append the response data to the DOM. You are familiar with HTTP requests, headers and can debug and profile XHR requests in something like postman or dev tools.",
            "weight": 4
        },{
            "name": "AJAX, API’s ",
            "description": "I can select DOM elements using vanilla Javascript. I can access and write to common properties such as innerHtml. ",
            "weight": 5
        },{
            "name": "Framework Madness",
            "description": "You have a good working knowledge of vanilla Javascript and have selected and used a major Javascript framework. Examples of frameworks might be Angular, React, Ember etc. You have used this framework on a completed production app or have used this framework to create and release a major feature on an app built by a team. Having done a tutorial or built a simple todo app in said framework does not qualify. It is given that you have the prior skills and fundamentals in Javascript. Being able to use Angular or React without understanding Javascript does not qualify you for this skill.",
            "weight": 6
        },{
            "name": "Working Knowledge",
            "description": "You use Javascript on a regular basis and have a good working knowledge of the available methods in the Javascript language. You understand the nuances of Javascript such as hoisting, scope.",
            "weight": 7
        },{
            "name": "Module Design Patterns",
            "description": "You are familiar with common module design patterns. Closures, IIFE’s, private and public methods. You can use module exports, requires etc to structure a Javascript app across multiple files.",
            "weight": 8
        },{
            "name": "Prototypical Inheritance and Object Oriented Javascript",
            "description": "You can create a javascript object and use prototypical inheritance. ",
            "weight": 9
        },{
            "name": "You Are A Recognized Industry Expert",
            "description": "You wrote a (well known) book, are a thought leader and speaker or are a core contributor to the language or created/core contributor to a library which is synonymous with the language (ie jquery, react etc).",
            "weight": 10
        }]
    }
}