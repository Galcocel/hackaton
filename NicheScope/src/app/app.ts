import { Component, OnInit, signal, ChangeDetectorRef  } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Nicho } from './nicho/nicho';
import { CommonModule } from '@angular/common';
import { BaseChartDirective  } from 'ng2-charts';
import { ChartConfiguration, ChartType } from 'chart.js';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import datosJson from './datos.json';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, Nicho, CommonModule, BaseChartDirective,FormsModule,HttpClientModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})


export class App implements OnInit{
  protected readonly title = signal('NicheScope');
  jsonCont = new Map();
  ayuda = ''
  objetoAMap(obj: any): Map<string, any> {
    const map = new Map<string, any>();
    if (obj && typeof obj === 'object' && !Array.isArray(obj)) {
      for (const [clave, valor] of Object.entries(obj as Record<string, any>)) {
        map.set(clave, (valor && typeof valor === 'object' && !Array.isArray(valor)) ? this.objetoAMap(valor) : valor);
      }
    }
    return map;
  }
  constructor(private http: HttpClient) {
    this.cargarJSON();
  }
  async cargarJSON() {
    try {
      //this.ayuda = "AAAAA"
      //this.jsonCont = new Map(Object.entries(datosJson)); // Convertimos objeto a Map
      this.jsonCont = this.objetoAMap(datosJson)
      console.log('Map cargado:', this.jsonCont);
    } catch (error) {
      //this.ayuda = "BBBBB"
      console.error('Error al cargar JSON:', error);
    }
  }
  value = 0;
  opcion = "Ninguna"
  nichos = ['Gym Enthusiast','Vegano','Conveniente/Express','Eco-Friendly','Familia Numerosa','Celíaco/Intolerancias','Gourmet/Premium']
  ciudades = ['Valencia','Madrid','Barcelona','Zaragoza','Cadiz']
  meses = ['12-24','01-25','02-25','03-25','04-25','05-25','06-25','07-25','08-25','09-25','10-25','11-25']
  map = new Map();
  datosUsuarios = new Map();
  datosCiudades = new Map();
  datosNichos = new Map();
  textoBuscar = '';
  barChartData: ChartConfiguration<'bar'>['data'] = {
    labels: this.nichos,
    datasets: [
      {
        data: [],
        label: 'null',
        backgroundColor: '#007bff'
      }
    ]
  };
  barChartOptions: ChartConfiguration<'bar'>['options'] = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Comparación de nichos' }
    }
  };
  barChartData2: ChartConfiguration<'bar'>['data'] = {
    labels: this.meses,
    datasets: [
      {
        data: [],
        label: 'null',
        backgroundColor: '#007bff'
      }
    ]
  };
  barChartOptions2: ChartConfiguration<'bar'>['options'] = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Historiograma de nichos' }
    }
  };

  
  randomize(){
    this.map = new Map();
    for (let i = 0; i < this.nichos.length; i++) {
      let map2 = new Map();
      map2.set("Name",this.nichos[i]);
      map2.set("Ranking",Math.floor(Math.random() * 10)+1);
      map2.set("Gains",Math.floor(Math.random() * 400)-200);
      this.map.set(this.nichos[i],map2);
    }
    //console.log("randomizado")
  }
  
  onClick() { 
    this.value++;
  }
  usuario(){
    this.opcion = "Usuario"
  }
  ciudad(){
    this.opcion = "Ciudad"
  }
  buscar(){
    if(this.opcion == "Usuario"){
      this.barChartData.datasets[0].data = this.datosUsuarios.get(this.textoBuscar)
    }else if(this.opcion == "Ciudad"){
      this.barChartData.datasets[0].data = this.datosCiudades.get(this.textoBuscar)
    }else{
      return
    }
    this.barChartData.datasets[0].label = this.textoBuscar
    this.barChartData = { ...this.barChartData };
    this.ayuda = this.datosUsuarios.get("1")[0]
  }
  nichoSelec(item:string){
    this.barChartData2.datasets[0].data = this.datosNichos.get(item);
    this.barChartData2.datasets[0].label = item;
    this.barChartData2 = { ...this.barChartData2 };

  }
  ngOnInit() {
    //this.ayuda = (this.jsonCont.get("analisis_mensual"));
    for (let i = 0; i < 10; i++) {
      this.datosUsuarios.set(i+"",Array.from({ length: this.nichos.length }, () => Math.floor(Math.random() * 100)))
    }
    for(let i in this.ciudades){
      this.datosCiudades.set(this.ciudades[i],Array.from({ length: this.nichos.length }, () => Math.floor(Math.random() * 100)))
    }
    //let mapAna = new Map(Object.entries(this.jsonCont.get("analisis_mensual")))
    //this.ayuda = (mapAna.get("2025-05")) + ""
    //for(let i = 0; i < mapAna.keys.length; i++){
    //  let aux = new Map(Object.entries(this.jsonCont.get("analisis_mensual")))
    //}
    for(let i in this.nichos){
      let arr = []
      arr[0] = Math.floor(Math.random() * 500)
      for(let j = 1; j < this.meses.length; j++){
        arr[j] = Math.max(arr[j-1] + Math.floor(Math.random() * 200) - 100,0) 
      }
      this.datosNichos.set(this.nichos[i],arr)
    }
    this.randomize();
  }
}
