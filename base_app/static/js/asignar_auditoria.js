const trashBin = document.getElementById('trash-bin');

Sortable.create(document.getElementById('contenedor-auditorias'), {
    group: {
        name: 'auditoria',
        pull: true,
        put: ['auditoria'] 
    },
    animation: 150,
    onRemove: function (evt) {
        const removedItem = evt.item;
        console.log(removedItem.textContent + ' ha sido removido del contenedor original');
    },
    onStart: function (evt) {
        trashBin.style.display = 'block';
    },
    onEnd: function (evt) {
        trashBin.style.display = 'none';
        if (evt.from === trashBin) {
            evt.from.removeChild(evt.item);
        }
    },
    onAdd: function (event) {
        const audit = event.item;
        const auditoriaId = audit.getAttribute('data-id'); 

        const nestedList = audit.querySelector('ul');
        if (nestedList && !Sortable.get(nestedList)) {
            Sortable.create(nestedList, {
                group: {
                    name: 'roles',
                    put: ['roles'] 
                },
                animation: 150,
                onStart: function (evt) {
                    trashBin.style.display = 'block';
                },
                onEnd: function (evt) {
                    trashBin.style.display = 'none';
                    if (evt.from === trashBin) {
                        evt.from.removeChild(evt.item);
                    }
                },
                onAdd: function (event) {
                    const role = event.item;
                    const roleId = role.getAttribute('data-role-id'); 

                    if (!role.querySelector('ul')) {
                        const employeeList = document.createElement('ul');
                        employeeList.classList.add('nested-list');
                        role.appendChild(employeeList);

                        Sortable.create(employeeList, {
                            group: {
                                name: 'empleados',
                                pull: true,
                                put: ['empleados']
                            },
                            animation: 150,
                            onStart: function (evt) {
                                trashBin.style.display = 'block';
                            },
                            onEnd: function (evt) {
                                trashBin.style.display = 'none';
                                if (evt.from === trashBin) {
                                    evt.from.removeChild(evt.item);
                                }
                            },
                            onAdd: function (event) {
                                const employeeItem = event.item;
                                const employeeId = employeeItem.getAttribute('data-employee-id');  
                                console.log('Empleado asignado:', employeeId);
                                fetch('/asignar/', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/x-www-form-urlencoded',
                                        'X-CSRFToken': getCookie('csrftoken')
                                    },
                                    body: `auditoria=${auditoriaId}&recurso=${employeeId}&rol=${roleId}`
                                })
                                .then(response => response.json())
                                .then(data => {
                                    if (data.status === 'success') {
                                        console.log('Asignación guardada');
                                    } else {
                                        console.error('Error en la asignación', data.message);
                                    }
                                })
                                .catch(error => console.error('Error en la petición', error));
                            },
                        });
                    } else {
                        const employeeList = role.querySelector('ul');
                        Sortable.get(employeeList).option('put', ['empleados']);
                    }
                }
            });
        } else {
            Sortable.get(nestedList).option('put', ['roles']);
        }
    },
});

// Sortable para roles dentro de auditoría
document.querySelectorAll('.auditoria-rol-recurso-call').forEach(function (auditoriaCall) {
    Sortable.create(auditoriaCall, {
        group: {
            name: 'roles',
            pull: true,
            put: ['roles']
        },
        animation: 150,
        onStart: function (evt) {
            trashBin.style.display = 'block';
        },
        onEnd: function (evt) {
            trashBin.style.display = 'none';
            if (evt.from === trashBin) {
                evt.from.removeChild(evt.item);
            }
        },
        onAdd: function (event) {
            const role = event.item;
            const roleId = role.getAttribute('data-role-id');  

            if (!role.querySelector('ul')) {
                const employeeList = document.createElement('ul');
                employeeList.classList.add('nested-list');
                role.appendChild(employeeList);

                Sortable.create(employeeList, {
                    group: {
                        name: 'empleados',
                        pull: true,
                        put: ['empleados'] 
                    },
                    animation: 150,
                    onStart: function (evt) {
                        trashBin.style.display = 'block';
                    },
                    onEnd: function (evt) {
                        trashBin.style.display = 'none';
                        if (evt.from === trashBin) {
                            evt.from.removeChild(evt.item);
                        }
                    },
                    onAdd: function (event) {
                        const employeeItem = event.item;
                        const employeeId = employeeItem.getAttribute('data-employee-id');  // ID del empleado
                        console.log('Empleado asignado en rol:', employeeId);
                    }
                });
            } else {
                const employeeList = role.querySelector('ul');
                Sortable.get(employeeList).option('put', ['empleados']);
            }
        }
    });
});

// Función para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

Sortable.create(trashBin, {
    group: {
        name: 'auditoria',
        pull: false, 
        put: true 
    },
    onAdd: function (evt) {
        evt.item.remove();
        console.log(evt.item.textContent + ' ha sido eliminado.');
    }
});

Sortable.create(document.getElementById('auditorias'), {
    group: {
        name: 'auditoria',
        pull: 'clone',
        put: false
    },
    animation: 150,
});

Sortable.create(document.getElementById('roles'), {
    group: {
        name: 'roles',
        pull: 'clone',
        put: false 
    },
    animation: 150,
});

// Empleados solo pueden ser movidos dentro de roles
document.querySelectorAll('.empleados').forEach(function (emp) {
    Sortable.create(emp, {
        group: {
            name: 'empleados',
            pull: 'clone',
            put: ['empleados'] 
        },
        animation: 150,
        onAdd: function (event) {
            const employeeItem = event.item;
            const employeeId = employeeItem.getAttribute('data-employee-id'); 
            console.log('Empleado movido:', employeeId);
        }
    });
});
