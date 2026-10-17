import { useEffect, useState } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import { api } from '../api';

type Act = {
  id: string;
  titulo: string;
  inicio: string;
  fin: string;
  prioridad: string;
  estado: string;
};

const colorFor = (p: string) =>
  p === 'alta' ? '#dc2626' : p === 'media' ? '#d97706' : '#059669';

export default function Calendar() {
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    api
      .get<Act[]>('/actividades')
      .then((list) => {
        setEvents(
          list.map((a) => ({
            id: a.id,
            title: a.titulo,
            start: a.inicio,
            end: a.fin,
            backgroundColor: colorFor(a.prioridad),
            borderColor: colorFor(a.prioridad),
          }))
        );
      })
      .catch(console.error);
  }, []);

  return (
    <div>
      <h1>Calendario</h1>
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="timeGridWeek"
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay',
        }}
        events={events}
        height="auto"
        locale="es"
      />
    </div>
  );
}