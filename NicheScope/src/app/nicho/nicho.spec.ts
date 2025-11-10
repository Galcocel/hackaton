import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Nicho } from './nicho';

describe('Nicho', () => {
  let component: Nicho;
  let fixture: ComponentFixture<Nicho>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Nicho]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Nicho);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
