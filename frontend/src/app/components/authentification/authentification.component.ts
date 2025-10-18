import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Auth } from '../../services/auth';
import { UserSessionService } from '../../services/user-session.service';

@Component({
  selector: 'app-authentification',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './authentification.component.html',
  styleUrls: ['./authentification.component.css']
})
export class AuthentificationComponent {
  isLoginMode = true;
  loginData = { email: '', password: '' };
  registerData = { first_name: '', last_name: '', email: '', password: '', specialist: false };
  errorMessage = '';

  constructor(private authService: Auth, private router: Router, private userSession: UserSessionService) {}

  onLogin() {
    this.errorMessage = '';
    this.authService.login(this.loginData.email, this.loginData.password).subscribe({
      next: (user: any) => {
        this.userSession.setUser(user);
        this.router.navigate(['/chatbot']);
      },
      error: (err: any) => {
        this.errorMessage = err.error?.message || 'Erreur de connexion';
      }
    });
  }

  onRegister() {
    this.errorMessage = '';
    const userData = {
      first_name: this.registerData.first_name,
      last_name: this.registerData.last_name,
      email: this.registerData.email,
      password: this.registerData.password,
      specialist: this.registerData.specialist
    };
    this.authService.register(userData).subscribe({
      next: (user: any) => {
        this.userSession.setUser(user);
        this.router.navigate(['/chatbot']);
      },
      error: (err: any) => {
        this.errorMessage = err.error?.message || "Erreur lors de l'inscription";
      }
    });
  }
}
