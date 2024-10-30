import { Component } from '@angular/core';

export interface Emloyee{
  id: string;
  dateOfBirth: string;
  password: string;
}

@Component({
  selector: 'app-snap-camera',
  standalone: true,
  imports: [],
  templateUrl: './snap-camera.component.html',
  styleUrl: './snap-camera.component.css'
})
export class SnapCameraComponent {

  Emloyees: Emloyee[]=[
    {id:"11", dateOfBirth:"12334", password:"123"},
    {id:"22", dateOfBirth:"12334", password:"456"},
    {id:"33", dateOfBirth:"12334", password:"097"}
  ]

  Allow(){
    alert('Hello camera...');
    console.log('it is working');
  }
}
