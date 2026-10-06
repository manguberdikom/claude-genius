package shop.cli;

public class Suppressed {

    @SuppressWarnings({"unchecked", "java:S106"})
    public void banner() {
        System.out.println("shop-cli 1.0");
        try {
            run();
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }

    public void quiet() {
        System.out.println("debug"); // NOSONAR: CLI chiqishi
        try {
            run();
        } catch (IllegalStateException e) {} // NOSONAR
        try {
            run();
        } catch (IllegalArgumentException e) {
            e.printStackTrace(); log("NOSONAR");
        }
    }

    @SuppressWarnings("java:S1148")
    private int count;

    // @SuppressWarnings("java:S106") izohda: hisoblanmaydi
    public void plain() {
        System.err.println("x");
    }
}
