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
          skillsets: response
        });
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  handleSkillsetSubmit: function(skillset) {
    console.log(skillset);
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
        this.setState({data: data});
        console.log(data);
        var updatedSkillsets = this.state.skillsets;
        console.log(updatedSkillsets);
        updatedSkillsets.push(data);
        console.log(updatedSkillsets);
        this.setState({skillsets: updatedSkillsets});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  render: function() {
    // var skillset = this.state.skillsets.map(function(obj) {
    //   return <Skillset skillset={obj} /> 
    // });
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
          })};
        </div>
        <SkillsetForm onSkillsetSubmit={this.handleSkillsetSubmit} />
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
  sendFormData: function () {
    var formData = {
      name: React.findDOMNode(this.refs.name).value,
      description: React.findDOMNode(this.refs.description).value
    }
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      type: 'POST',
      data: formData,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
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


ReactDOM.render(
<Profile url="http://dev.tshape.com:8000/api/profiles/1/skillsets/" />,
  document.getElementById('tshape')
);
