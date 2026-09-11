from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Student
from .forms import StudentForm


@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_courses = Student.objects.values('course').distinct().count()
    students = Student.objects.all().order_by('-id')[:5]

    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'students': students,
    }

    return render(request, 'students/dashboard.html', context)


@login_required
def student_list(request):
    search = request.GET.get('search', '')
    students = Student.objects.all()

    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(student_id__icontains=search) |
            Q(course__icontains=search)
        )

    context = {
        'students': students,
        'search': search,
    }

    return render(request, 'students/student_list.html', context)


@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = StudentForm()

    context = {
        'form': form,
        'title': 'Add Student',
    }

    return render(request, 'students/student_form.html', context)


@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = StudentForm(instance=student)

    context = {
        'form': form,
        'title': 'Edit Student',
    }

    return render(request, 'students/student_form.html', context)


@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()
        return redirect('student_list')

    context = {
        'student': student,
    }

    return render(
        request,
        'students/student_confirm_delete.html',
        context
    )