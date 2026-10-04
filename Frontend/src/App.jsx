import Header from "./components/Header";
import MachineForm from "./components/MachineForm";

function App() {
  return (
    <main className="flex h-screen flex-col overflow-hidden bg-slate-100 p-4 text-slate-900">
      <div className="mx-auto flex w-full max-w-6xl flex-1 flex-col">
        <Header />
        <MachineForm />
      </div>
    </main>
  );
}

export default App;
