import {Component, OnInit, OnDestroy} from '@angular/core';
import {Subscription} from 'rxjs';
import {RadioApiService} from './radio/radio-api.service';
import {Radio} from './radio/radio.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'app';
  radioListSubs: Subscription;
  radioList: Radio[];

  constructor(private radioApi: RadioApiService) {
  }

  ngOnInit() {
    this.radioListSubs = this.radioApi
      .getData()
      .subscribe(res => {
          this.radioList = res;
        },
        console.error
      );
  }

  ngOnDestroy() {
    this.radioListSubs.unsubscribe();
  }
}
