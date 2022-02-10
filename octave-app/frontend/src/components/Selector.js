import React from 'react'

class ActivityButton extends React.Component {
    changeClass(id) {
        if(document.getElementById(id).classList.contains("Selected")){
            document.getElementById(id).classList.remove("Selected");
        }else{
            document.getElementById(id).classList.add("Selected");
        }
    }

    render() {
        return(
            <button id={this.props.name} onClick={() => this.changeClass(this.props.name)}>{this.props.name}</button>
        )
    }
}

export default ActivityButton