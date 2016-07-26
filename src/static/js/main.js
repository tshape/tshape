var pathArray = window.location.pathname.split( '/' );
var userId = pathArray[2];
var profileApi = "http://dev.tshape.com:8000/api/profiles/" + userId + "/";

console.log(userId);
console.log(profileApi);

var Profile = React.createClass({
  getInitialState: function() {
    return {
      skillsets: [],
      profileName: null,
    };
  },
  componentDidMount: function() {
     $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(response) {
        console.log("profiles/:id/skillsets/ API Call:", response);
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
    console.log("handleSkillsetPut", skillset.id);
    var csrfToken = Cookies.get('csrftoken');
    $.ajax({
      url: profileApi,
      dataType: 'json',
      type: 'PUT',
        headers: {
        'X-CSRFToken': csrfToken
      },
      data: {"skillsets": [{"id": skillset.id}]},
      success: function(data) {
        var items = this.state.skillsets;
        items.push(data);
        this.setState({
          skillsets: items
        });
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  handleSkillsetCreate: function(skillset) {
    console.log("handleSkillsetCreate", skillset);
    var csrfToken = Cookies.get('csrftoken');
    $.ajax({
      url: "http://dev.tshape.com:8000/api/skillsets/",
      dataType: 'json',
      type: 'POST',
        headers: {
        'X-CSRFToken': csrfToken
      },
      data: skillset,
      success: function(data) {
        console.log("handleSkillsetCreate AJAC success", data);
        var items = this.state.skillsets;
        items.push(data);
        this.setState({
          skillsets: items
        });
        this.handleSkillsetPut(data);
      }.bind(this),
      error: function(xhr, status, err) {
        console.error("handleSkillsetCreate AJAX error", this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  handleSkillsetDelete: function(skillset) {
    console.log("handleSkillsetDelete", skillset);
    var csrfToken = Cookies.get('csrftoken');
    $.ajax({
      url: "http://dev.tshape.com:8000/api/skillsets/",
      dataType: 'json',
      type: 'POST',
        headers: {
        'X-CSRFToken': csrfToken
      },
      data: skillset.id,
      success: function(data) {
        var items = this.state.skillsets.filter(function(item){
          return skillset.id !== item.id;
        });
        this.setState({
          skillsets: items
        });
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  remove: function(skillset) {
    var items = this.state.skillsets.filter(function(item){
      return skillset.id !== item.id;
    });
    this.setState({
      skillsets: items
    });
  },
  render: function() {
    console.log("Profile:render - skillsets", this.state.skillsets);
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
            return <Skillset skillset={obj} key={obj.id} /> 
          })}
        </div>
        <SkillsetForm onSkillsetSubmit={this.handleSkillsetCreate} />
        <div className="skillsetlist">
          <h3>Skillset List</h3>
          <ul>
            return <SkillsetListItems skillsets={this.state.skillsets} onRemove={this.handleSkillsetDelete} />
          </ul>
        </div>
      </div>
    );
  }
});

var Skillset = React.createClass({
    render() {
      // var skill = this.props.skillset.skills.map(function(obj) {
      //   return <Skill skill={obj} /> 
      // });
      return (
        <div className="tshape__skillset" id={this.props.skillset.id}>
          <div className="tshape__skillset-heading">{this.props.skillset.name}</div>
          <div className="tshape__skill"></div>
        </div>
      );
    }
});

var Skill = React.createClass({
    render: function(){
      // {this.props.skill.description}
        return <li>skill</li>;
    }
});

var SkillsetForm = React.createClass({
  getInitialState: function() {
    return {
      name: '', 
      description: ''
    };
  },
  handleNameFieldChange: function(e) {
    this.setState({name: e.target.value});
  },
  handleDescriptionFieldChange: function(e) {
    this.setState({description: e.target.value});
  },
  handleSubmit: function(e) {
    e.preventDefault();
    var name = this.state.name.trim();
    var description = this.state.description.trim();
    if (!name || !description) {
      return;
    }
    this.props.onSkillsetSubmit({name: name, description: description});
    this.setState({name: '', description: ''});
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
        <input
          type="text"
          ref="description"
          placeholder="Skillset Description"
          value={this.state.description}
          onChange={this.handleDescriptionFieldChange}
        />
        <input type="submit" value="Post" />
      </form>
    );
  }
});

var SkillsetListItems = React.createClass({
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



ReactDOM.render(
<Profile url={profileApi} />,
  document.getElementById('tshape')
);
