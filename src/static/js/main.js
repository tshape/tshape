var pathArray = window.location.pathname.split( '/' );
var userId = pathArray[2];
var profileApi = "http://dev.tshape.com:8000/api/profiles/" + userId + "/";
var csrfToken = Cookies.get('csrftoken');

var profile = {};
var allSkillsets = [];
var allSkills = [];
var mySkillsets = [];
var mySkills = [];
var tshape = [];
var hashMap = {
  "107": { "name": "Java" },
  "801": { "name": "Poo" },
  "666": { "name": "Life" }
};
var allSkillsetsHash = {};   
var mySkillsetsHash = {};

console.log("User ID:", userId);

// React App
var Profile = React.createClass({
  getInitialState: function() {
    return {
      activeSkillset: {"id": null},
      mySkillsets: [],
      mySkills: [],
      allSkillsets: [],
      allSkills: [],
      tshape: [],
      profileName: null,
      hashMap: hashMap,
      mySkillsetsHash: {},
      allSkillsetsHash: {}
    };
  },
  createTshape: function() {
    console.log("Creating Tshape...");
    for (var i = 0; i < profile.skillset_ids.length; i++) { 
      _.forEach(mySkillsets, function(skillsetValue, skillsetKey) {
        if (skillsetValue.id === profile.skillset_ids[i]) {
          delete skillsetValue.skill_ids; 
          skillsetValue.skills = [];
          tshape.push(skillsetValue); 
          _.forEach(mySkills, function(skillValue, skillKey) {
            if (skillValue.skillset_id === skillsetValue.id) {
               skillsetValue.skills.push(skillValue);
            }
          })
        }
      })
    }
    console.log(tshape);

    //Create mySkillsetshash 
    _.forEach(mySkillsets, function(v, k) {
      mySkillsetsHash[v.id] = v;
    });

    //Create allSkillsetshash 
    _.forEach(allSkillsets, function(v, k) {
      allSkillsetsHash[v.id] = v;
      mySkillsetsHash[v.id] ? v.active = true : v.active = false;
    });

    console.log(allSkillsetsHash);

    // Update React state
    this.setState({
      tshape: tshape,
      mySkillsets: mySkillsets,
      mySkills: mySkills,
      mySkillsetsHash: mySkillsetsHash,
      allSkillsets: allSkillsets,
      allSkills: allSkills,
      allSkillsetsHash: allSkillsetsHash
    });
  },
  componentDidMount: function() {
    
    $.when(ajaxProfile(), ajaxMySkills(), ajaxMySkillsets(), ajaxAllSkills(), ajaxAllSkillsets()).done(function(a1,a2,a3,a4,a5) {
      console.log("API Calls Complete");

      // console.log("API Response > ajaxProfile", a1[0]);
      profile = a1[0];
      // console.log("API Response > ajaxMySkills", a2[0]);
      mySkills = a2[0];
      // console.log(a3[0]);
      mySkillsets = a3[0];
      // console.log(a4[0]);
      allSkills = a4[0];
      // console.log(a5[0]);
      allSkillsets = a5[0];

      this.createTshape();
    }.bind(this));

    // Get the Profile Object
    function ajaxProfile() {
      return $.ajax({
        url: "http://dev.tshape.com:8000/api/profiles/1/",
        dataType: 'json',
        cache: false,
        success: function(response) {

        }.bind(this),
        error: function(xhr, status, err) {
          console.error(this.props.url, status, err.toString());
        }.bind(this)
      });
    }

    // Get My Skills Object
    function ajaxMySkills() {
      return $.ajax({
        url: "http://dev.tshape.com:8000/api/profiles/1/skills/",
        dataType: 'json',
        success: function(response) {

        }.bind(this),
        error: function(xhr, status, err) {
          console.error(this.props.url, status, err.toString());
        }.bind(this)
      });
    }

    // Get My Skillsets Object
    function ajaxMySkillsets() {
      return $.ajax({
        url: "http://dev.tshape.com:8000/api/profiles/1/skillsets/",
        dataType: 'json',
        success: function(response) {

        }.bind(this),
        error: function(xhr, status, err) {
          console.error(this.props.url, status, err.toString());
        }.bind(this)
      });
    }

     // Get All Skills Object
    function ajaxAllSkills() {
      return $.ajax({
        url: "http://dev.tshape.com:8000/api/skills/",
        dataType: 'json',
        success: function(response) {

        }.bind(this),
        error: function(xhr, status, err) {
          console.error(this.props.url, status, err.toString());
        }.bind(this)
      });
    }

    // Get All Skillsets Object
    function ajaxAllSkillsets() {
      return $.ajax({
        url: "http://dev.tshape.com:8000/api/skillsets/",
        dataType: 'json',
        success: function(response) {

        }.bind(this),
        error: function(xhr, status, err) {
          console.error(this.props.url, status, err.toString());
        }.bind(this)
      });
    }
  },
  handleSkillsetCreate: function(skillset) {
    console.log("handleSkillsetCreate", skillset);

    // If the skillset already exists, go straight to the PUT function
    if (allSkillsetsHash[skillset.id]) {
      console.log("Skillset already exists! Adding to Profile");
      this.handleSkillsetPut(skillset);
    } else {
      // If the skillset does not exist, POST the skillset to the API
      // On success this will return a new skillset object with a valid ID
      $.ajax({
        url: "http://dev.tshape.com:8000/api/skillsets/",
        dataType: 'json',
        type: 'POST',
          headers: {
          'X-CSRFToken': csrfToken
        },
        data: skillset,
        success: function(data) {
          console.log("handleSkillsetCreate AJAX success", data);
          this.handleSkillsetPut(data);
        }.bind(this),
        error: function(xhr, status, err) {
          console.error("handleSkillsetCreate AJAX error", this.props.url, status, err.toString());
        }.bind(this)
      });
    }
  },
  handleSkillsetPut: function(skillset) {
    console.log("handleSkillsetPut", skillset);

    if (mySkillsetsHash[skillset.id]) {
      // do nothing.
    } else {
      // add the skillset to mySkillsetsHash
      mySkillsetsHash[skillset.id] = skillset
      // add a skills array to the skillset
      mySkillsetsHash[skillset.id].skills = [];
      // update react state
      this.setState({
        mySkillsetsHash: mySkillsetsHash
      });
      console.log("me", this.state.mySkillSetHash)
      // set an active flag on the skillset in allSkillsetsHash
      allSkillsetsHash[skillset.id].active = true;
      this.setState({
        allSkillsetsHash: allSkillsetsHash
      });
      // Generate an array of skillset ID's to PUT to API
      var mySkillsetIds = Object.keys(this.state.mySkillsetsHash).map(function(value, key) {
        return mySkillsetsHash[value].id
      });
    }

    console.log("PUT skillsets", mySkillsetIds);
    // PUT the new skillset to the users profile via the API
    // The API accepts this format: {"skillset_ids": [1,2,3]}
    var data = JSON.stringify({"skillset_ids": mySkillsetIds});

    $.ajax({
      url: profileApi,
      method: "PUT",
      headers: {
        'X-CSRFToken': csrfToken,
        "content-type": "application/json"
      },
      data: data,
      success: function(data) {
        console.log("handleSkillsetPut AJAX Success", data);
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  handleSkillsetRemove: function(skillset) {
    console.log("handleSkillsetRemove", skillset);

    delete mySkillsetsHash[skillset.id]
    this.setState({
      mySkillsetsHash: mySkillsetsHash
    });

    allSkillsetsHash[skillset.id].active = false;
    this.setState({
      allSkillsetsHash: allSkillsetsHash
    });

    var mySkillsetIds = Object.keys(this.state.mySkillsetsHash).map(function(value, key) {
      return mySkillsetsHash[value].id
    });

    var data = JSON.stringify({"skillset_ids": mySkillsetIds});

    // POST new skillsets object to API
    $.ajax({
      url: profileApi,
      method: "PUT",
      headers: {
        'X-CSRFToken': csrfToken,
        "content-type": "application/json"
      },
      data: data,
      success: function(data) {
        console.log("handleSkillsetRemove AJAX Success", data);
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  handleSkillCreate: function(skill) {
    console.log("handleSkillCreate", skill);

    var data = JSON.stringify({"name": skill.name, "skillset_id": skill.skillset_id});

    $.ajax({
      url: "http://dev.tshape.com:8000/api/skills/",
      dataType: 'json',
      type: 'POST',
        headers: {
        'X-CSRFToken': csrfToken,
        "content-type": "application/json"
      },
      data: data,
      success: function(data) {
        console.log("handleSkillCreate AJAX success", data);
        this.handleSkillPut(data);
      }.bind(this),
      error: function(xhr, status, err) {
        console.error("handleSkillCreate AJAX error", this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  handleSkillPut: function(skill) {
    console.log("handleSkillPut", skill);
    var newTshape = this.state.tshape;

    // Check if the skill is already selected
    var activeSkillset = this.state.activeSkillset;

    _.forEach(activeSkillset.skills, function(skillItem) {
      if (skillItem.id  === skill.id) {
        return false;
      }
    });

    _.forEach(newTshape, function(skillset) {
      if (skill.skillset_id !== null && skill.skillset_id  === skillset.id) {
        skillset.skills.push(skill);
      }
    });

    this.setState({
      tshape: newTshape
    });

    var newAllSkills = this.state.allSkills
    newAllSkills.push(skill);

    this.setState({
      allSkills: newAllSkills
    });

    var mySkillIds = []
    _.forEach(newTshape, function(skillsetItem) {
      _.forEach(skillsetItem.skills, function(skillItem) {
        mySkillIds.push(skillItem.id);
      });
    });
    
    var data = JSON.stringify({"skill_ids": mySkillIds});
    console.log("handleSkillPut skill_ids", mySkillIds)
    $.ajax({
      url: profileApi,
      method: "PUT",
      headers: {
        'X-CSRFToken': csrfToken,
        "content-type": "application/json"
      },
      data: data,
      success: function(data) {
        console.log("handleSkillPut AJAX Success", data);
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  handleSkillRemove: function(skill) {
    console.log("handleSkillRemove", skill);

    // Remove the skill form the tshape state
    var newTshape = this.state.tshape;
    _.forEach(newTshape, function(skillsetItem) {
      _.remove(skillsetItem.skills, function(skillItem) {
        return skillItem.id === skill.id
      })
    });

    this.setState({
      tshape: newTshape
    });


    // remove the skill from the skill_ids and PUT
    var mySkillIds = []
    _.forEach(newTshape, function(skillsetItem) {
      _.forEach(skillsetItem.skills, function(skillItem) {
        mySkillIds.push(skillItem.id);
      });
    });

    var data = JSON.stringify({"skill_ids": mySkillIds});
    console.log("handleSkillPut skill_ids", mySkillIds)

    // remove the skill from the mySkills state
    var newMySkills = this.state.mySkills;
     _.remove(newMySkills, function(skillItem) {
      return skillItem.id === skill.id
    })

    this.setState({
      mySkills: newMySkills
    });

    // POST new skillsets object to API
    $.ajax({
      url: profileApi,
      method: "PUT",
      headers: {
        'X-CSRFToken': csrfToken,
        "content-type": "application/json"
      },
      data: data,
      success: function(data) {
        console.log("handleSkillRemove AJAX Success", data);
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  setActiveSkillset: function(skillset) {
    console.log("setActiveSkillset", skillset);
    this.setState({
      activeSkillset: skillset
    });
  },
  render: function() {
    var skills = this.state.skills;
    return (
      <div>
        <div className="tshape">
          <div className="tshape__header">
              <h2 className="tshape__role">UI Engineer</h2>
              <h3 className="tshape__user">Robert Austin</h3>
              <div className="tshape__badges">
                  <span className="tshape__github"><a href="#"><i className="fa fa-github" aria-hidden="true"></i></a></span>
                  <span className="tshape__linkedin"><a href="#"><i className="fa fa-linkedin-square" aria-hidden="true"></i></a></span>
              </div>
          </div>
          <div className="tshape__middle">
            {Object.keys(this.state.mySkillsetsHash).map(function(value, key) {
              return <SkillsetTshape key={key} skillset={this.state.mySkillsetsHash[value]} isActive={this.state.activeSkillset.id === value.id ? "active" : "inactive" } />
            }.bind(this))}
          </div>
        </div>
        <div>
          <hr />
          <h2>Add Skillsets</h2>
          <div className="skillsets">
            <h3>My Skillsets</h3>
            {Object.keys(this.state.mySkillsetsHash).map(function(value, key) {
              return <MySkillsetItem skillset={this.state.mySkillsetsHash[value]} key={key} activeSkillset={this.state.activeSkillset} setActiveSkillset={this.setActiveSkillset} onRemove={this.handleSkillsetRemove} />
            }.bind(this))}
            <h3>All Skillsets</h3>
            {Object.keys(this.state.allSkillsetsHash).map(function(value, key) {
              return <AllSkillsetItem skillset={this.state.allSkillsetsHash[value]} key={key} onAdd={this.handleSkillsetCreate} />
            }.bind(this))};
            <h3>Add Custom Skillset</h3>
            <AddSkillset onSkillsetSubmit={this.handleSkillsetCreate} />
          </div>
          <hr />
          <h2>Add Skills</h2>
          <div className="skills">
              <ListMySkills skillsets={this.state.tshape} allSkills={this.state.allSkills} activeSkillset={this.state.activeSkillset} onRemove={this.handleSkillRemove} />
              <h3>All Skills</h3>
              <ListAllSkills skillsets={this.state.tshape} allSkills={this.state.allSkills} activeSkillset={this.state.activeSkillset} onAdd={this.handleSkillPut} />
              <AddSkill skillsets={this.state.skillsets} onSkillSubmit={this.handleSkillCreate} activeSkillset={this.state.activeSkillset}/>
          </div>
        </div>
      </div>
    );
  }
});

var MySkillsetItem = React.createClass({
  setActive: function(item) {
    return function(e) {
      e.preventDefault();
      return this.props.setActiveSkillset(item);
    }.bind(this);
  },
  remove: function(item) {
    return function(e) {
      e.preventDefault();
      return this.props.onRemove(item);
    }.bind(this);
  },
  render: function() {
    return (
      <li className={"skillset__item skillset__item--tag " + (this.props.activeSkillset.id === this.props.skillset.id ? "active" : "inactive") } onClick={this.setActive(this.props.skillset)}>
        <span>{this.props.skillset.name}</span>
        <a href="#" onClick={this.remove(this.props.skillset)}>remove</a>
      </li>
    )
  }
});
var AllSkillsetItem = React.createClass({
  add: function(item) {
    return function(e) {
      e.preventDefault();
      return this.props.onAdd(item);
    }.bind(this);
  },
  render: function() {
    if (this.props.skillset.active) {
      return (
        <li className={"skillset__item"} >
          <span>{this.props.skillset.name}</span>
        </li>
      )
    } else {
      return (
        <li className={"skillset__item"}>
          <a href="#" className="skillset__link" onClick={this.add(this.props.skillset)}>{this.props.skillset.name}</a>
        </li>
      )
    }
  }
});
var SkillsetTshape = React.createClass({
    render: function(){
      return (
        <div className={"tshape__skillset " + this.props.isActive} id={this.props.skillset.id}>
          <div className="tshape__skillset-heading">{this.props.skillset.name}</div>
          {this.props.skillset.skills.map(function(value, key) {
            return <SkillTshape key={key} skill={value} />
          })}
        </div>
      );
    }
});
var SkillTshape = React.createClass({
    render: function(){
      return (
        <div className="tshape__skill" id={this.props.skill.id}>
          <div className="tshape__skillname">{this.props.skill.name}</div>
        </div>
      );
    }
});
var AddSkillset = React.createClass({
  getInitialState: function() {
    return {
      name: ''
    };
  },
  handleNameFieldChange: function(e) {
    this.setState({name: e.target.value});
  },
  handleSubmit: function(e) {
    e.preventDefault();
    var name = this.state.name.trim();
    if (!name) {
      return;
    }
    this.props.onSkillsetSubmit({name: name});
    this.setState({name: ''});
  },
  render: function() {
    return (
      <form className="commentForm" onSubmit={this.handleSubmit}>
        <input
          type="text"
          ref="name"
          placeholder="Skillset Name"
          value={this.state.name}
          onChange={this.handleNameFieldChange}
        />
        <input type="submit" value="Post" />
      </form>
    );
  }
});
var AddSkill = React.createClass({
  getInitialState: function() {
    return {
      skillset_id: '',
      name: ''
    };
  },
  handleSkillNameFieldChange: function(e) {
    this.setState({name: e.target.value});
  },
  handleSkillDescriptionFieldChange: function(e) {
    this.setState({description: e.target.value});
  },
  handleSkillsetIdFieldChange: function(e) {
    this.setState({skillset_id: e.target.value});
  },
  handleSubmit: function(e) {
    e.preventDefault();
    var name = this.state.name.trim();
    var skillset_id = this.props.activeSkillset.id;

    if (!name || !skillset_id) {
      return;
    }
    this.props.onSkillSubmit({name: name, skillset_id: skillset_id});
    this.setState({name: '', skillset_id: ''});
  },
  render: function() {
    return (
      <form className="commentForm" onSubmit={this.handleSubmit}>
        <input
          type="text"
          ref="name"
          placeholder="Skill Name"
          value={this.state.name}
          onChange={this.handleSkillNameFieldChange}
        />
        <input type="submit" value="Post" />
      </form>
    );
  }
});
var ListMySkillsets = React.createClass({
  setActive: function(item) {
    return function(e) {
      e.preventDefault();
      return this.props.setActiveSkillset(item);
    }.bind(this);
  },
  remove: function(item) {
    return function(e) {
      e.preventDefault();
      return this.props.onRemove(item);
    }.bind(this);
  },
  render: function() {
    var items = this.props.skillsets.map(function(item, i) {
      return (
        <li className={"skillset__item skillset__item--tag " + (this.props.activeSkillset.id === item.id ? "active" : "inactive") } key={i} onClick={this.setActive(item)}>
          <span>{item.name}</span>
          <a href data-id={item.id} className="remove-filter" onClick={this.remove(item)}>remove</a>
        </li>
      );
    }.bind(this));

    return <ul>{items}</ul>;
  }
});
var ListAllSkillsets = React.createClass({
  add: function(item) {
    return function(e) {
      e.preventDefault();
      return this.props.onAdd(item);
    }.bind(this);
  },
  remove: function(item) {
    return function(e) {
      e.preventDefault();
      return this.props.onRemove(item);
    }.bind(this);
  },
  render: function() {
    var items = this.props.allSkillsets.map(function(item, i) {
      if (_.some(this.props.skillsets, { 'id': item.id })) {
        return (
          <li className="skillset__item skillset__item--assigned" key={"all-skillsets-item-" + i}>
            <span>{item.name}</span>
          </li>
        );
      } else {
        return (
          <li className="skillset__item skillset__item--unassigned" key={i}>
          <a href data-id={item.id} className="skillset__link" onClick={this.add(item)}>{item.name}</a>
          </li>
        );
      }
    }.bind(this));
    return <ul>{items}</ul>;
  }
});
var ListMySkills = React.createClass({
  setActive: function(item) {
    return function(e) {
      e.preventDefault();
      return this.props.setActive(item);
    }.bind(this);
  },
  remove: function(item) {
    return function(e) {
      e.preventDefault();
      return this.props.onRemove(item);
    }.bind(this);
  },
  render: function() {
    if (this.props.activeSkillset.id === null) {
      return <p>Please select a Skillset first</p>
    } else if (this.props.activeSkillset.skills.length === 0) {
      return <p>This skillset currently has no skills</p>
    } else {
      var items = this.props.activeSkillset.skills.map(function(item, i) {
        return (
          <li className="skill__item skill__item--tag " key={i} >
            <span>{item.name}</span>
             <a href data-id={item.id} className="skill__link skill__link--remove" onClick={this.remove(item)}>X</a>
          </li>
        );
      }.bind(this))
    }
    return <div>{items}</div>;
  }
});
var ListAllSkills = React.createClass({
  add: function(item) {
    return function(e) {
      e.preventDefault();
      return this.props.onAdd(item);
    }.bind(this);
  },
  remove: function(item) {
    return function(e) {
      e.preventDefault();
      return this.props.onRemove(item);
    }.bind(this);
  },
  render: function() {
    var items = this.props.allSkills.filter(function(item, i) {
      if (this.props.activeSkillset.id !== null && this.props.activeSkillset.id === item.skillset_id) {
        return true;
      }
    }.bind(this));
    console.log(items);
    items = items.map(function(item, i) {
       if (_.some(this.props.skillsets, { 'id': item.id })) {
        return (
          <li className="skill__item skill__item--assigned" key={i}>
            <span>{item.name}</span>
          </li>
        );
      } else {
         return (
          <li className="skill__item skill__item--unassigned" key={i}>
            <a href="#" data-id={item.id} className="skill__link" onClick={this.add(item)}>{item.name}</a>
          </li>
        );
      }
    }.bind(this));
    if (items.length === 0) {
      return <p>This skillset currently has no all skills</p>
    } else {
      return <ul>{items}</ul>
    }
  }
});

ReactDOM.render(
<Profile url={profileApi} />,
  document.getElementById('tshape')
);
