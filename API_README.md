# GET Routes

#### Quick Reference
api/users/ - return a list of user objects with related profile model

api/profiles/ - returns list of profile objects without related models
api/profiles/:id/ - returns a profile object with related ids

api/profiles/:id/skillsets/ - returns a list of skillset objects specific to the profile, with all related ids
api/profiles/:id/skillsets/:id/ - returns a skillset object specific to the profile, with all related ids

api/profiles/:id/skills/ - returns a list of skill objects specific to the profile with related ids
api/profiles/:id/skills/:id/ - returns a skill object specific to the profile with related ids

api/skillsets/ - returns a list of all skillset objects with related ids
api/skillsets/:id/ - returns a skillset object with related skill ids

api/skillsets/:id/skills/ - returns a list of skill objects
api/skillsets/:id/skills/:id/ - returns a skill object, specific to the skillset

api/skills/ - returns a list of skill objects
api/skills/:id/ - returns a skill object


#### API Routes with examples

api/users/ - return a list of user objects with related profile model

ie. [
  {
    "id": 1,
    "email": "jackgarza@hotmail.com",
    "is_staff": false,
    "is_active": true,
    "date_joined": "2016-07-23T22:29:26.855331Z",
    "first_name": "",
    "last_name": "",
    "profile": {
      "user_id": 1,
      "first_name": "test profile 1",
      "last_name": "BLACH",
      "title": "Engineer, civil (consulting)",
      "description": "",
      "years_experience": 10
    }
  }
]

api/profiles/ - returns list of profile objects without related models

ie. [
  {
    "user_id": 1,
    "first_name": "test profile 1",
    "last_name": "BLACH",
    "title": "Engineer, civil (consulting)",
    "description": "",
    "years_experience": 10
  }
]

api/profiles/:id/ - returns a profile object with related ids

ie. {
  "user_id": 1,
  "first_name": "test profile 1",
  "last_name": "BLACH",
  "title": "Engineer, civil (consulting)",
  "description": "",
  "years_experience": 10,
  "skillset_ids": [
    5,
    1
  ],
  "skill_ids": [
    5,
    7
  ]
}

api/profiles/:id/skillsets/ - returns a list of skillset objects specific to the profile, with all related ids

ie. [
  {
    "id": 5,
    "name": "BLACH",
    "description": "",
    "verified": true,
    "weight": 0,
    "skill_ids": [
      54,
      52
    ]
  }
]

api/profiles/:id/skillsets/:id/ - returns a skillset object specific to the profile, with all related ids

ie. {
    "id": 5,
    "name": "BLACH",
    "description": "",
    "verified": true,
    "weight": 0,
    "skill_ids": [
      54,
      52
    ]
  }

api/profiles/:id/skills/ - returns a list of skill objects specific to the profile with related ids

ie. [
  {
    "id": 5,
    "name": "Parker, David and Li",
    "description": "Molestias accusantium quos quis a omnis. Quos atque minus quis voluptates libero. Velit quisquam amet architecto itaque reprehenderit. Ipsa iste dolores dolore laborum possimus consequatur magni.",
    "verified": true,
    "skillset_id": 5
  }
]

api/profiles/:id/skills/:id/ - returns a skill object specific to the profile with related ids

ie. {
    "id": 5,
    "name": "Parker, David and Li",
    "description": "Molestias accusantium quos quis a omnis. Quos atque minus quis voluptates libero. Velit quisquam amet architecto itaque reprehenderit. Ipsa iste dolores dolore laborum possimus consequatur magni.",
    "verified": true,
    "skillset_id": 5
  }

api/skillsets/ - returns a list of all skillset objects with related ids

ie. [
  {
    "id": 11,
    "name": "Algorithms",
    "description": "",
    "verified": true,
    "weight": 0,
    "skill_ids": [
      3,
      9,
      2
    ]
  }
]

api/skillsets/:id/ - returns a skillset object with related skill ids

ie. {
  "id": 1,
  "name": "JavaScript",
  "description": "",
  "verified": false,
  "weight": 0,
  "skill_ids": [
    79,
    77,
    76,
    73
  ]
}

api/skillsets/:id/skills/ - returns a list of skill objects

ie. [
  {
    "id": 79,
    "name": "Allen Ltd",
    "description": "",
    "verified": true,
    "skillset_id": 1
  }
]

api/skillsets/:id/skills/:id/ - returns a skill object, specific to the skillset

ie. {
  "id": 79,
  "name": "Allen Ltd",
  "description": "",
  "verified": true,
  "skillset_id": 1
}

api/skills/ - returns a list of skill objects

ie. [
  {
    "id": 91,
    "name": "Adams-Beck",
    "description": "",
    "verified": false,
    "skillset_id": 15
  }
]

api/skills/:id/ - returns a skill object

ie. {
    "id": 91,
    "name": "Adams-Beck",
    "description": "",
    "verified": false,
    "skillset_id": 15
  }
