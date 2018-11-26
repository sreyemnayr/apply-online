import { Component, OnInit } from '@angular/core';
import {ApiService} from "../api.service";

@Component({
  selector: 'app-student-list',
  templateUrl: './student-list.component.html',
  styleUrls: ['./student-list.component.css']
})
export class StudentListComponent implements OnInit {
  students: Array<object> = [];

  constructor(private apiService: ApiService) { }

  ngOnInit() {
    this.getStudents();
  }

  public getStudents(){
    this.apiService.getStudents().subscribe((data: Array<object>) => {
      this.students = data;
      console.log(data)
    })
  }

}
