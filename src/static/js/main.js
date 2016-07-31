var pathArray = window.location.pathname.split( '/' );
var userId = pathArray[2];
var profileApi = "http://dev.tshape.com:8000/api/profiles/" + userId + "/";
var csrfToken = Cookies.get('csrftoken');
var allSkillsets = [];
var allSkills = [];
console.log("User ID:", userId);

// Store all skillsets in an array
$.ajax({
  url: "http://dev.tshape.com:8000/api/skillsets/",
  dataType: 'json',
  success: function(response) {
    allSkillsets = response; 

  }.bind(this),
  error: function(xhr, status, err) {
    console.error(this.props.url, status, err.toString());
  }.bind(this)
});

// Store all skills in an array
// $.ajax({
//   url: "http://dev.tshape.com:8000/api/skills/",
//   dataType: 'json',
//   success: function(response) {
//     allSkills = response; 

//   }.bind(this),
//   error: function(xhr, status, err) {
//     console.error(this.props.url, status, err.toString());
//   }.bind(this)
// });

// React App
var Profile = React.createClass({
  getInitialState: function() {
    return {
      skillsets: [],
      skills: [],
      profileName: null,
    };
  },
  componentDidMount: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(response) {
        console.log("profiles/:id/ API Call:", response);
        this.setState({
          skillsets: response.skillsets,
          skills: response.skills
        });
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  handleSkillsetPut: function(skillset) {
    console.log("handleSkillsetPut", skillset);

    var items = this.state.skillsets;
    items.push(skillset);

    // Update React state
    this.setState({
      skillsets: items
    });

    var data = JSON.stringify({"skillsets": items});
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
  handleSkillsetCreate: function(skillset) {
    console.log("handleSkillsetCreate", skillset);

    var newSkillset = _.find(allSkillsets, { 'name': skillset.name})
    console.log(newSkillset);

    // Check if the skillset the user is attempting to add already exists
    if (newSkillset) {
      console.log("Skillset already exists! Adding to Profile");
      this.handleSkillsetPut(newSkillset);
    } else {
      console.log("Skillset does not exist! Adding to All Skillsets and Profile");
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
  handleSkillsetRemove: function(skillset) {
    console.log("handleSkillsetRemove", skillset);

    // Remove the skillset from skillsets array
    var items = this.state.skillsets.filter(function(item){
      return skillset.id !== item.id;
    });

    // Update React state
    this.setState({
      skillsets: items
    });

    // Prepare skillset array for sending
    items = JSON.stringify({"skillsets": items});

    // POST new skillsets object to API
    $.ajax({
      url: profileApi,
      method: "PUT",
      headers: {
        'X-CSRFToken': csrfToken,
        "content-type": "application/json"
      },
      data: items,
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

    // var newSkill = _.find(allSkills, { 'name': skill.name})
    // console.log(newSkill);

    // Check if the skill the user is attempting to add already exists
    // if (newSkill) {
    //   console.log("Skill already exists! Adding to Profile");
    //   this.handleSkillsetPut(newSkill);
    // } 

    var data = JSON.stringify({"name": skill.name, "description": skill.description});

    $.ajax({
      url: "http://dev.tshape.com:8000/api/skills/",
      dataType: 'json',
      type: 'POST',
        headers: {
        'X-CSRFToken': csrfToken
      },
      data: data,
      success: function(data) {
        console.log("handleSkillCreate AJAX success", data);
        this.handleSkillsetPut(data);
      }.bind(this),
      error: function(xhr, status, err) {
        console.error("handleSkillCreate AJAX error", this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  handleSkillPut: function(skill) {
    console.log("handleSkillPut", skill);

    var items = this.state.skills;
    items.push(skill);

    // Update React state
    this.setState({
      skills: items
    });

    var data = JSON.stringify({"skills": items});
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

    // Remove the skillset from skillsets array
    var items = this.state.skills.filter(function(item){
      return skill.id !== item.id;
    });

    // Update React state
    this.setState({
      skills: items
    });

    // Prepare skillset array for sending
    var data = JSON.stringify({"skills": items});

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
  render: function() {
    console.log("Profile:render - skillsets", this.state.skillsets);
    var skills = this.state.skills;
    return (
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
          {this.state.skillsets.map(function(obj) {
            var skillsInSkillset = _.filter(skills, { 'skillset_id': obj.id });
            return <Skillset skillset={obj} skills={skillsInSkillset} key={obj.id} /> 
          })}
        </div>
        <h2>Add Skillset</h2>
        <AddSkillset onSkillsetSubmit={this.handleSkillsetCreate} />
        <h2>Add Skill</h2>
        <AddSkill onSkillSubmit={this.handleSkillCreate} skillsets={this.state.skillsets} />
        <div className="list__skills">
          <h3>Skillset List</h3>
          <ul>
            return <ListSkillsets skillsets={this.state.skillsets} onRemove={this.handleSkillsetRemove} />
          </ul>
        </div>
        <div className="skillsetlist">
          <h3>Skill List</h3>
          <ul>
            return <ListSkills skills={this.state.skills} onRemove={this.handleSkillRemove} />
          </ul>
        </div>
      </div>
    );
  }
});

var Skillset = React.createClass({
    render: function(){
      return (
        <div className="tshape__skillset" id={this.props.skillset.id}>
          <div className="tshape__skillset-heading">{this.props.skillset.name}</div>
          {this.props.skills.map(function(obj) {
            return <Skill skill={obj} key={obj.id}  />
          })}
        </div>
      );
    }
});

var Skill = React.createClass({
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
      name: '',
      description: ''
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
    var description = this.state.description;
    var skillset_id = this.state.skillset_id;

    if (!name || !skillset_id || !description) {
      return;
    }
    this.props.onSkillSubmit({name: name, description: description, skillset_id: skillset_id});
    this.setState({name: '', skillset_id: '', description: ''});
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
        <input
          type="text"
          ref="description"
          placeholder="Skill Description"
          value={this.state.description}
          onChange={this.handleSkillDescriptionFieldChange}
        />
       <input
          type="text"
          ref="skillset_id"
          placeholder="Skillset ID"
          value={this.state.skillset_id}
          onChange={this.handleSkillsetIdFieldChange}
        />
        <input type="submit" value="Post" />
      </form>
    );
  }
});


var ListSkillsets = React.createClass({
  remove: function(item) {
    return function(e) {
      e.preventDefault();
      return this.props.onRemove(item);
    }.bind(this);
  },

  render: function() {
    var items = this.props.skillsets.map(function(item, i) {
      return (
        <li key={i}>
          <span>{item.name}</span>
          <a href data-id={item.id} className="remove-filter" onClick={this.remove(item)}>remove</a>
        </li>
      );
    }.bind(this));

    return <ul>{items}</ul>;
  }
});


var ListSkills = React.createClass({
  remove: function(item) {
    return function(e) {
      e.preventDefault();
      return this.props.onRemove(item);
    }.bind(this);
  },
  render: function() {
    console.log(this.props.skills);
    var items = this.props.skills.map(function(item, i) {
      return (
        <li key={i}>
          <span>{item.name}</span>
          <a href data-id={item.id} className="remove-filter" onClick={this.remove(item)}>remove</a>
        </li>
      );
    }.bind(this));
    return (<ul>{items}</ul>);
  }
});



ReactDOM.render(
<Profile url={profileApi} />,
  document.getElementById('tshape')
);
