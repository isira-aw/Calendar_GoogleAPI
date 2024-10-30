import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { DateDetailsComponent } from './date-details/date-details.component';
import { SnapCameraComponent } from './snap-camera/snap-camera.component';
import { UploadSectionComponent } from './upload-section/upload-section.component';


export const routes: Routes = [
    {path :'', component :HomeComponent},
    {path :'date', component :DateDetailsComponent},
    {path :'camera' , component :SnapCameraComponent},
    {path :'upload',component :UploadSectionComponent}
];
