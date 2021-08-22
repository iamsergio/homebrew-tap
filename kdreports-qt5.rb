class KdreportsQt5 < Formula
  desc "A Qt5-based library for creating printable reports"
  homepage "https://github.com/KDAB/KDReports"
  url "https://github.com/KDAB/KDReports/releases/download/kdreports-2.0.0/kdreports-2.0.0.tar.gz"
  sha256 "24f68fc93d7565eb7077fbfc9cff2b37fdf44611d5b281e6ef0aa3a9636b78b4"
  head "https://github.com/KDAB/KDReports.git"

  depends_on "qt5" => "with-d-bus"
  depends_on "cmake" => :build

  def install
    system "cmake", ".", *std_cmake_args
    system "make"
    system "make", "install"
  end

  test do
    system "make", "test"
  end
end
