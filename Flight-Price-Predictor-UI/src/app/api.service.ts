import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

//const appUrl ='http://127.0.0.1:5000'
const appUrl ='https://flight-price-predictor-api.herokuapp.com'
const urlEncodedhttpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient,) { }

  getSources() {
    const url: string = appUrl+'/getSources';
    return this.http.get(url);
  }
  getDestinations() {
    const url: string = appUrl+'/getDestinations';
    return this.http.get(url);
  }
  getAirlines() {
    const url: string = appUrl+'/getAirlines';
    return this.http.get(url);
  }
  getStopages() {
    const url: string = appUrl+'/getStopages';
    return this.http.get(url);
  }

  predictPrice(requestData) {
    const url: string = appUrl+'/predictPrice';
    return this.http.post(url, requestData, urlEncodedhttpOptions);
  }
}
