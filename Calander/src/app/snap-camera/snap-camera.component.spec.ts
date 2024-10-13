import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SnapCameraComponent } from './snap-camera.component';

describe('SnapCameraComponent', () => {
  let component: SnapCameraComponent;
  let fixture: ComponentFixture<SnapCameraComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SnapCameraComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SnapCameraComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
