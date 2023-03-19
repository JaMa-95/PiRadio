import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import 'rxjs/add/operator/catch';
import {API_URL} from '../env';
import {Radio} from './radio.model';

@Injectable()
export class RadioApiService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any) {
    return Observable.throw(err.message || 'Error: Unable to complete request.');
  }

  // GET list of public, future events
  getData(): Observable<Radio[]> {
    return this.http
      .get(`${API_URL}/data`)
      .catch(RadioApiService._handleError);
  }
}