import React from 'react';
import '../assets/css/home.css';
import Navbar from '../components/navbar';


export default function Home(){
  
  return (
    <div>
      <Navbar />

    <div className="home_container">
      <div className="home_header">
        <h1 className='home_h1'>Calendar</h1>
      </div>
      <div className="home_content">
        <div className="home_calendar">
        {[...Array(31).keys()].map((day) => (
  <div key={day} className="home_day">
    {day + 1}
  </div>
))}
        </div>
        <div className="home_sidebar">
          <div className="home_top-box">
            
          </div>
          <div className="home_bottom-box">

          </div>

          <div className="home_buttonsDiv">
            <button className='home_buttons'>Button 1</button>
            <button className='home_buttons'>Button 2</button>
            <button className='home_buttons'>Button 3</button>
          </div>
        </div>
      </div>
    </div>
    </div>
  );
}
