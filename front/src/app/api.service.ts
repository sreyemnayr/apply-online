import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  API_URL = 'http://localhost:8000/api/v1';

  constructor(private httpClient: HttpClient) { }

  getStudents(){
    return this.httpClient.get(`${this.API_URL}/students/`);
  }

}
