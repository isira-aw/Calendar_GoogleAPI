import React, { useState, useEffect } from "react";
import axios from "axios";
import "../assets/css/home.css";

const Home = () => {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [events, setEvents] = useState([]);

  // Function to fetch events for the current month
  const fetchEvents = async () => {
    const year = currentMonth.getFullYear();
    const month = currentMonth.getMonth() + 1; // Months are 0-indexed
    try {
      const response = await axios.get(
        `http://localhost:8000/calendar/events?year=${year}&month=${month}`
      );
      console.log("Fetched Events:", response.data.events);
      setEvents(response.data.events);
    } catch (error) {
      console.error("Error fetching events:", error);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, [currentMonth]);

  const getDaysInMonth = (month, year) => new Date(year, month + 1, 0).getDate();

  const generateCalendarDays = () => {
    const days = [];
    const year = currentMonth.getFullYear();
    const month = currentMonth.getMonth();
    const totalDays = getDaysInMonth(month, year);

    // Add empty slots before the first day
    const firstDayIndex = new Date(year, month, 1).getDay();
    for (let i = 0; i < firstDayIndex; i++) {
      days.push({ day: null });
    }

    // Add all days in the month
    for (let day = 1; day <= totalDays; day++) {
      days.push({ day });
    }

    return days;
  };

  const handleMonthChange = (direction) => {
    const newMonth = new Date(
      currentMonth.getFullYear(),
      currentMonth.getMonth() + direction,
      1
    );
    setCurrentMonth(newMonth);
  };

  const getEventsForDay = (day) => {
    const date = `${currentMonth.getFullYear()}-${String(
      currentMonth.getMonth() + 1
    ).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    return events.filter((event) => event.date === date);
  };

  const calendarDays = generateCalendarDays();

  return (
    <div className="calendar-container">
      <div className="calendar-header">
        <button onClick={() => handleMonthChange(-1)}>&lt;</button>
        <h2>
          {currentMonth.toLocaleString("default", { month: "long" })}{" "}
          {currentMonth.getFullYear()}
        </h2>
        <button onClick={() => handleMonthChange(1)}>&gt;</button>
      </div>
      <div className="calendar-grid">
        {/* Weekday Headers */}
        <div className="weekday-header">Sun</div>
        <div className="weekday-header">Mon</div>
        <div className="weekday-header">Tue</div>
        <div className="weekday-header">Wed</div>
        <div className="weekday-header">Thu</div>
        <div className="weekday-header">Fri</div>
        <div className="weekday-header">Sat</div>

        {/* Calendar Days */}
        {calendarDays.map((dayObj, index) => (
          <div key={index} className="calendar-day">
            {dayObj.day && (
              <>
                <span>{dayObj.day}</span>
                <div className="events">
                  {getEventsForDay(dayObj.day).map((event, idx) => (
                    <div key={idx} className="event">
                      {event.summary}
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
