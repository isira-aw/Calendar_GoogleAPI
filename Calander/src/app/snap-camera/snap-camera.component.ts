import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';

export interface Emloyee{
  id: string;
  dateOfBirth: string;
  password: string;
}

@Component({
  selector: 'app-snap-camera',
  templateUrl: './snap-camera.component.html',
  standalone: true,
  imports: [ MatSlideToggleModule ,CommonModule]
})
export class SnapCameraComponent {

  emloyees: Emloyee[]=[
    {id:"11", dateOfBirth:"12334", password:"123"},
    {id:"22", dateOfBirth:"12334", password:"456"},
    {id:"33", dateOfBirth:"12334", password:"097"}
  ]

  Allow(){
    alert('Hello camera...');
    console.log('it is working');
  }
}
