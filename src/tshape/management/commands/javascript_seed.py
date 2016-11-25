from skills.models import Skill
from skillsets.models import Skillset

__all__ = ["JAVASCRIPT_SKILLS"]


JAVASCRIPT_SKILLS = {
    Skillset: {
        Skill: [{
            "name": "Snippets",
            "description": "I can insert Javascript scripts into a page. I understand how to embed script tags in the body and header. I can make simple modifications to basic Javascript code such as modifying a variable, modifying the output of text.",
            "weight": 1
        }, {
            "name": "Basic Functions & Conditional Logic",
            "description": "Without using Google I can write a basic function that accepts an argument and outputs a value. I can write both the function and then call the function. I understand how to load this script into a basic html page and see it execute in a browser.",
            "weight": 2
        },{
            "name": "Arrays & Object Literals",
            "description": "Has a good understanding of arrays. Can create, add, delete and access an index in an array. sort and generally manipulate and transform array data structures using Javascript. Create an object literal. Write and read properties of the object using dot notation.",
            "weight": 3
        },{
            "name": "Iteration",
            "description": "I am confident iterating through arrays and objects. I can write a for, forEach methods without referencing Google. Both using for, foreach. I can access object keys and values ",
            "weight": 4
        },{
            "name": "DOM Manipulation & AJAX",
            "description": "I can select DOM elements using vanilla Javascript. I can access and write to common properties such as innerHtml. ",
            "weight": 5
        },{
            "name": "Closures",
            "description": "I understand Javascript scope and how IIFE’s and closures can be used to create private and public scope.",
            "weight": 6
        },{
            "name": "Callbacks",
            "description": "I understand callbacks, and can use a callback. ",
            "weight": 7
        },{
            "name": "Module Design Patterns",
            "description": "You are familiar with common module patterns.",
            "weight": 8
        },{
            "name": "Prototypical Inheritance and Object Oriented Javascript",
            "description": "I can create a javascript object and use prototypical inheritance.",
            "weight": 9
        },{
            "name": "You are a recognized industry expert",
            "description": "You wrote a (well known) book, are a core contributor to the language or created a open source library which is synonymous with the language (ie jquery, react etc).",
            "weight": 10
        }]
    }
}