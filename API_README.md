## Quick Reference

#### GET Routes

**api/users/** - return a list of user objects with related profile model

**api/profiles/** - returns list of profile objects without related models
**api/profiles/:id/** - returns a profile object with related ids

**api/profiles/:id/skillsets/** - returns a list of skillset objects specific to the profile, with all related ids
**api/profiles/:id/skillsets/:id/** - returns a skillset object specific to the profile, with all related ids

**api/profiles/:id/skills/** - returns a list of skill objects specific to the profile with related ids
**api/profiles/:id/skills/:id/** - returns a skill object specific to the profile with related ids

**api/skillsets/** - returns a list of all skillset objects with related ids
**api/skillsets/:id/** - returns a skillset object with related skill ids

**api/skillsets/:id/skills/** - returns a list of skill objects
**api/skillsets/:id/skills/:id/** - returns a skill object, specific to the skillset

**api/skills/** - returns a list of skill objects
**api/skills/:id/** - returns a skill object


#### POST Routes

**api/users/**
* *required field(s):*
    *  email (string)
* *optional field(s):*
  * is_staff (boolean)
  * is_active (boolean)

**api/skillsets/**
* *required field(s):*
  * name (string)
* *optional field(s):*
  * description (string)
  * verified (boolean)
  * weight (integer)
  * skill_ids (list of integers)

**api/skills/**
* *required field(s):*
  * name (string)
  * skillset_id (integer)
* *optional field(s):*
  * description (string)
  * verified (boolean)
  * weight (integer)


#### PUT Routes

**api/users/:id/**
* *optional field(s):*
  * email (string)
  * is_staff (boolean)
  * is_active (boolean)

**api/profiles/:id/**
 * *optional field(s):*
   * first_name (string)
   * last_name (string)
   * title (string)
   * description (string)
   * years_experience (integer)
   * skillset_ids (list of integers)
   * skill_ids (list of integers)

**api/skillsets/:id/**
* *optional field(s):*
  * name (string)
  * description (string)
  * verified (boolean)
  * weight (integer)
  * skill_ids (list of integers)

**api/skills/:id/**
* *optional field(s):*
  * name (string)
  * description (string)
  * verified (boolean)


#### DELETE Routes

**api/users/:id/**
**api/profiles/:id/**
**api/skillsets/:id/**
**api/skills/:id/**


#### API Routes with examples

**api/users/** - return a list of user objects with related profile model

```
[
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
```

**api/profiles/** - returns list of profile objects without related models

```
[
  {
    "user_id": 1,
    "first_name": "test profile 1",
    "last_name": "BLACH",
    "title": "Engineer, civil (consulting)",
    "description": "",
    "years_experience": 10
  }
]
```

**api/profiles/:id/** - returns a profile object with related ids

```
{
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
```

**api/profiles/:id/skillsets/** - returns a list of skillset objects specific to the profile, with all related ids

```
[
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
```

**api/profiles/:id/skillsets/:id/** - returns a skillset object specific to the profile, with all related ids

```
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
```

**api/profiles/:id/skills/** - returns a list of skill objects specific to the profile with related ids

```
[
  {
    "id": 5,
    "name": "Parker, David and Li",
    "description": "",
    "verified": true,
    "skillset_id": 5
  }
]
```

**api/profiles/:id/skills/:id/** - returns a skill object specific to the profile with related ids

```
{
    "id": 5,
    "name": "Parker, David and Li",
    "description": "",
    "verified": true,
    "skillset_id": 5
}
```

**api/skillsets/** - returns a list of all skillset objects with related ids

```
[
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
```

**api/skillsets/:id/** - returns a skillset object with related skill ids

```
{
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
```

**api/skillsets/:id/skills/** - returns a list of skill objects

```
[
  {
    "id": 79,
    "name": "Allen Ltd",
    "description": "",
    "verified": true,
    "skillset_id": 1
  }
]
```

**api/skillsets/:id/skills/:id/** - returns a skill object, specific to the skillset

```
{
  "id": 79,
  "name": "Allen Ltd",
  "description": "",
  "verified": true,
  "skillset_id": 1
}
```

**api/skills/** - returns a list of skill objects

```
[
  {
    "id": 91,
    "name": "Adams-Beck",
    "description": "",
    "verified": false,
    "skillset_id": 15
  }
]
```

**api/skills/:id/** - returns a skill object

```
{
    "id": 91,
    "name": "Adams-Beck",
    "description": "",
    "verified": false,
    "skillset_id": 15
}
```
