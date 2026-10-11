import { Component, Input, Output, EventEmitter, forwardRef, HostListener, ElementRef } from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

export interface CalendarDay {
  date: number;
  disabled: boolean;
  selected: boolean;
  fullDate: Date;
}

@Component({
  selector: 'app-date-picker',
  templateUrl: './date-picker.component.html',
  styleUrls: ['./date-picker.component.scss'],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => DatePickerComponent),
      multi: true
    }
  ]
})
export class DatePickerComponent implements ControlValueAccessor {
  @Input() label: string = '';
  @Input() placeholder: string = 'Select a date';
  @Input() minDate: Date | string = new Date();
  
  @Output() dateChange = new EventEmitter<Date>();

  selectedDate: Date | null = null;
  selectedDateFormatted: string = '';
  calendarOpen: boolean = false;

  currentYear: number = new Date().getFullYear();
  currentMonth: number = new Date().getMonth();
  calendarDays: CalendarDay[] = [];

  onChange: any = () => {};
  onTouched: any = () => {};

  constructor(private elementRef: ElementRef) {
    this.generateCalendarDays();
  }

  get currentMonthName(): string {
    const monthNames = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    return monthNames[this.currentMonth];
  }

  writeValue(value: any): void {
    if (value) {
      this.selectedDate = new Date(value);
      this.currentYear = this.selectedDate.getFullYear();
      this.currentMonth = this.selectedDate.getMonth();
      this.formatSelectedDate();
    } else {
      this.selectedDate = null;
      this.selectedDateFormatted = '';
    }
    this.generateCalendarDays();
  }

  registerOnChange(fn: any): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: any): void {
    this.onTouched = fn;
  }

  toggleCalendar(): void {
    this.calendarOpen = !this.calendarOpen;
    if (this.calendarOpen) {
      this.generateCalendarDays();
    }
  }

  prevMonth(): void {
    this.currentMonth--;
    if (this.currentMonth < 0) {
      this.currentMonth = 11;
      this.currentYear--;
    }
    this.generateCalendarDays();
  }

  nextMonth(): void {
    this.currentMonth++;
    if (this.currentMonth > 11) {
      this.currentMonth = 0;
      this.currentYear++;
    }
    this.generateCalendarDays();
  }

  selectDate(day: CalendarDay): void {
    if (day.disabled || day.date === 0) return;

    this.selectedDate = new Date(this.currentYear, this.currentMonth, day.date);
    this.formatSelectedDate();
    this.calendarOpen = false;
    this.onChange(this.selectedDate);
    this.onTouched();
    this.dateChange.emit(this.selectedDate);
    this.generateCalendarDays();
  }

  private formatSelectedDate(): void {
    if (!this.selectedDate) {
      this.selectedDateFormatted = '';
      return;
    }
    this.selectedDateFormatted = this.selectedDate.toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  }

  generateCalendarDays(): void {
    let min: Date;
    if (typeof this.minDate === 'string' && this.minDate) {
      min = new Date(this.minDate);
    } else if (this.minDate instanceof Date) {
      min = this.minDate;
    } else {
      min = new Date();
    }
    min.setHours(0, 0, 0, 0);

    const firstDay = new Date(this.currentYear, this.currentMonth, 1);
    const startDay = firstDay.getDay();
    const daysInMonth = new Date(this.currentYear, this.currentMonth + 1, 0).getDate();

    const days: CalendarDay[] = [];

    for (let i = 0; i < startDay; i++) {
      days.push({ date: 0, disabled: true, selected: false, fullDate: new Date() });
    }

    for (let d = 1; d <= daysInMonth; d++) {
      const cellDate = new Date(this.currentYear, this.currentMonth, d);
      const isDisabled = cellDate < min;
      const isSelected = !!this.selectedDate && cellDate.toDateString() === this.selectedDate.toDateString();
      days.push({
        date: d,
        disabled: isDisabled,
        selected: isSelected,
        fullDate: cellDate
      });
    }

    this.calendarDays = days;
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent): void {
    if (!this.elementRef.nativeElement.contains(event.target)) {
      this.calendarOpen = false;
    }
  }
}
