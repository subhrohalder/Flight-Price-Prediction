import { Component, OnInit } from '@angular/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { NgxSpinnerService } from "ngx-spinner";
import { ApiService } from '../api.service';
import * as moment from 'moment';




@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})


export class HomePageComponent implements OnInit {



  sourceList: any[] = [];
  destinationList: any[] = []
  stopages: any[] = []
  airlineList: any[] = []
  predictedPrice: any[]
  highestPrice: any
  lowestPrice: any
  averagePrice: any
  actualPrice: any

  priceCard: boolean = false




  flightDetailsForm = new FormGroup({
    departureDate: new FormControl('', Validators.required),
    arrivalDate: new FormControl('', Validators.required),
    source: new FormControl('', Validators.required),
    destination: new FormControl('', Validators.required),
    stopage: new FormControl('', Validators.required),
    airlineName: new FormControl('', Validators.required),
  });


  constructor(private spinner: NgxSpinnerService, private services: ApiService) { }

  ngOnInit() {
    this.spinner.show();
    this.getSources();
    this.getAirlines();
    this.getStopages();
  }



  private getSources() {
    this.services.getSources().subscribe((response: any) => {
      this.sourceList = response.sources
    }, error => {
      console.log(error);
    });
  }

  private getDestinations() {
    this.services.getDestinations().subscribe((response: any) => {
      this.destinationList = response.destinations
      this.destinationList = this.destinationList.filter(val => val !== this.flightDetailsForm.value.source);
    }, error => {
      console.log(error);
    });
  }


  private getAirlines() {
    this.services.getAirlines().subscribe((response: any) => {
      this.airlineList = response.airlines
    }, error => {
      console.log(error);
    });
  }

  private getStopages() {
    this.services.getStopages().subscribe((response: any) => {
      this.stopages = response.stopages
      this.spinner.hide();
    }, error => {
      console.log(error);
      this.spinner.hide();
    });
  }



  onSubmit() {
    this.priceCard = true
    // console.table(this.flightDetailsForm.value)
    this.spinner.show();
    let reqBody = {
      airlineName: this.flightDetailsForm.value.airlineName,
      destination: this.flightDetailsForm.value.destination,
      source: this.flightDetailsForm.value.source,
      stopage: this.flightDetailsForm.value.stopage,
      arrivalDate: moment(moment(this.flightDetailsForm.value.arrivalDate)).format("YYYY-MM-DDTHH:mm"),
      departureDate: moment(moment(this.flightDetailsForm.value.departureDate)).format("YYYY-MM-DDTHH:mm"),
    }

    this.services.predictPrice(reqBody).subscribe((response: any) => {
      //  console.log(response)
      this.predictedPrice = response
      //  console.log(this.predictedPrice)
      //  console.log(this.flightDetailsForm.value.airlineName)
      this.actualPrice = this.predictedPrice.find(o => o.airline === this.flightDetailsForm.value.airlineName)
      this.highestPrice = this.predictedPrice.reduce((prev, current) => (+prev.predictedPrice > +current.predictedPrice) ? prev : current);
      this.lowestPrice = this.predictedPrice.reduce((prev, current) => (+prev.predictedPrice < +current.predictedPrice) ? prev : current);
      this.averagePrice = +(this.predictedPrice.reduce((a, { predictedPrice }) => a + predictedPrice, 0) / this.predictedPrice.length).toFixed(1);

      //  console.log(this.actualPrice,this.highestPrice,this.lowestPrice,this.averagePrice)

      this.spinner.hide();
    }, error => {
      console.log(error);
      this.spinner.hide();
    });



    // setTimeout(() => {
    //   /** spinner ends after 5 seconds */
    //   this.spinner.hide();
    // }, 5000);
  }

  sourceChange() {
    this.getDestinations();
    this.flightDetailsForm.controls['destination'].setValue("");

  }


}
