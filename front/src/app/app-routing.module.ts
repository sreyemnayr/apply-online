import {NgModule} from "@angular/core";
import {Routes, RouterModule} from "@angular/router";
import {AccountListComponent} from "./account-list/account-list.component";
import {AccountCreateComponent} from "./account-create/account-create.component";
import {StudentListComponent} from "./student-list/student-list.component";
import {StudentCreateComponent} from "./student-create/student-create.component";

const routes: Routes = [
  {path: '', redirectTo: 'students', pathMatch: 'full'},
  {path: 'accounts', component: AccountListComponent},
  {path: 'create-account', component: AccountCreateComponent},
  {path: 'students', component: StudentListComponent},
  {path: 'create-student', component: StudentCreateComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }

