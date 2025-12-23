interface Props {
  children: React.ReactNode;
}

const CenteredLayout = ({ children }: Props) => {
  return (
    <div className="h-screen w-full">
      <div className="flex h-full items-center justify-center bg-gray-100">
        {children}
      </div>
    </div>
  );
};

export default CenteredLayout;
