import React from 'react';
import '../assets/css/navbar.css';

export default function Navbar() {
    
    document.addEventListener('DOMContentLoaded', () => {
        const menuToggle = document.getElementById('menuToggle');
        const navLinks = document.getElementById('navLinks');
  
        menuToggle.addEventListener('click', () => {
          navLinks.classList.toggle('show');
        });
      });

  return (
    <nav class="navbar">
    <a href="#" class="brand">Navbar</a>
    <button class="menu-toggle" id="menuToggle">☰</button>
    <ul class="nav-links" id="navLinks">
      <li><a href="#">Home</a></li>
      <li><a href="#">Features</a></li>
      <li><a href="#">Pricing</a></li>
      <li><a href="#" class="disabled" aria-disabled="true">Disabled</a></li>
    </ul>
  </nav>

  );
}
