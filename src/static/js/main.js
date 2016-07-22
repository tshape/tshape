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
        console.log(response);
        this.setState({
          skillsets: response[0].skillsets,
          profileName: response[0].profileName
        });
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  render: function() {
    var skillset = this.state.skillsets.map(function(obj) {
      return <Skillset skillset={obj} /> 
    });
    return (
      <div className="profile">
        {this.state.profileName}
        {skillset}
      </div>
    );
  }
});

var Skillset = React.createClass({
    render() {
      var skill = this.props.skillset.skills.map(function(obj) {
        return <Skill skill={obj} /> 
      });
      return (
          <div>
          {this.props.skillset.name}
          {skill}
          </div>
      );
    }
});

var Skill = React.createClass({
    render: function(){
        return <li>{this.props.skill.description}</li>;
    }
});

var SkillSetForm = React.createClass({
  getInitialState: function() {
    return {author: '', text: ''};
  },
  handleAuthorChange: function(e) {
    this.setState({author: e.target.value});
  },
  handleTextChange: function(e) {
    this.setState({text: e.target.value});
  },
  handleSubmit: function(e) {
    e.preventDefault();
    var author = this.state.author.trim();
    var text = this.state.text.trim();
    if (!text || !author) {
      return;
    }
    // TODO: send request to the server
    this.setState({author: '', text: ''});
  },
  render: function() {
    return (
      <form className="commentForm" onSubmit={this.handleSubmit}>
        <input
          type="text"
          placeholder="Your name"
          value={this.state.author}
          onChange={this.handleAuthorChange}
        />
        <input
          type="text"
          placeholder="Say something..."
          value={this.state.text}
          onChange={this.handleTextChange}
        />
        <input type="submit" value="Post" />
      </form>
    );
  }
});


ReactDOM.render(
  <Profile url="http://localhost:9000/profiles" welcomeMsg="test" />,
  document.getElementById('container')
);
