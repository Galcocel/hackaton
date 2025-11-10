import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-nicho',
  imports: [],
  templateUrl: './nicho.html',
  styleUrl: './nicho.css',
})

export class Nicho {
  @Input() mymap = new Map();
  name = '';
  ranking = '';
  gains = '';
  ngOnInit() {
    this.name = this.mymap.get("Name");
    this.ranking = this.mymap.get("Ranking");
    let aux = this.mymap.get("Gains");
    if (aux >= 0){
      this.gains = "+" + aux + "%"
    }else{
      this.gains = aux + "%"
    }

  }
}
