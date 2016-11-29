from skills.models import Skill
from skillsets.models import Skillset

__all__ = ["PHP_SKILLS"]


PHP_SKILLS = {
    Skillset: {
        Skill: [{
            "name": "Basic PHP Templating",
            "description": "You can make basic changes to a PHP template file. You can print variables, and sometimes modify obvious code using trial and error.",
            "weight": 1
        }, {
            "name": "PHP Environment",
            "description": "You am familiar with the LAMP stack. You can setup a local environment using terminal or a GUI tool like MAMP/XAMP. You can modify php.ini and httpd.conf. You can setup an SQL database (say mySQL) and view the database tables. You can import and dump databases. You can deploy a PHP website or CMS.",
            "weight": 2
        },{
            "name": "Basic Functions & Conditional Logic",
            "description": "You can write a basic function that accepts an argument and outputs a value. You can write both the function and then call the function.",
            "weight": 3
        },{
            "name": "Arrays and Associative Arrays",
            "description": "You have a good understanding of arrays and hashes. Can create, add, delete and access an index in an array. sort and generally manipulate and transform array data structures using PHP",
            "weight": 4
        },{
            "name": "Iteration",
            "description": "I am confident iterating through arrays and objects. I can write a for, foreach methods without referencing Google. Both using for, foreach. I can access object keys and values",
            "weight": 5
        },{
            "name": "Knowledge of Common Functions",
            "description": "You are familiar with common string and array functions in the standard PHP library. Due to my experience with PHP I have a good knowledge of available functions that are available and can easily navigate the PHP documentation to find and implement new functions when appropriate.",
            "weight": 6
        },{
            "name": "Object Oriented PHP",
            "description": "You are familiar with and have written object oriented PHP. You have written a major feature or app using OOP methodologies.",
            "weight": 7
        },{
            "name": "Strong Ability In a Popular Framework",
            "description": "You have used a popular PHP framework to implement a real production app, or have worked on an app in a business environment that uses a popular PHP framework. Frameworks such as  Laravel, Symfony, CodeIgniter, Zend Framework or similar (sorry if your favourite framework is not mentioned).",
            "weight": 8
        },{
            "name": "Security Compliance",
            "description": "Understanding of security (esp. SQL injection, XSS). Strong knowledge of the common PHP or web server exploits and their solutions. Ability to write PHP code that is secure.",
            "weight": 9
        }, {
            "name": "You Are A Recognized Industry Expert",
            "description": "You wrote a (well known) book, are a thought leader or speaker. You may be a core contributor to the language or you have created and or make major contributions to a library which is synonymous with the language.",
            "weight": 10
        }]
    }
}